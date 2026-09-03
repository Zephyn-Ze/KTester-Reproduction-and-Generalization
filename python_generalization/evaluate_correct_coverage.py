import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from experiment_targets import get_target


PROJECT_DIR = Path(__file__).resolve().parent


def run_pytest(arguments, coverage_file=None):
    environment = os.environ.copy()
    if coverage_file is not None:
        environment["COVERAGE_FILE"] = str(coverage_file)
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", *arguments],
        cwd=PROJECT_DIR,
        env=environment,
        capture_output=True,
        text=True,
    )


def collect_nodeids(test_file):
    result = run_pytest([str(test_file), "--collect-only", "-q"])
    nodeids = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if "::test_" not in line:
            continue
        collected_path, separator, test_name = line.partition("::")
        if not (PROJECT_DIR / collected_path).exists() and Path(test_file).exists():
            line = f"{test_file}{separator}{test_name}"
        nodeids.append(line)
    return result.returncode == 0, nodeids, result.stdout + result.stderr


def test_method_results(nodeids):
    results = []
    for nodeid in nodeids:
        result = run_pytest([nodeid, "-q"])
        results.append(
            {
                "nodeid": nodeid,
                "passed": result.returncode == 0,
                "returncode": result.returncode,
                "output": result.stdout + result.stderr,
            }
        )
    return results


def target_coverage(report_path, target):
    report = json.loads(report_path.read_text())
    suffix = target.file.as_posix()
    for filename, details in report["files"].items():
        if filename.endswith(suffix):
            functions = details.get("functions", {})
            if target.function not in functions:
                raise RuntimeError(
                    f"Coverage report does not contain function {target.function!r}"
                )
            summary = functions[target.function]["summary"]
            statements = summary["num_statements"]
            covered_statements = summary["covered_lines"]
            branches = summary.get("num_branches", 0)
            covered_branches = summary.get("covered_branches", 0)
            return {
                "covered_statements": covered_statements,
                "statements": statements,
                "statement_percent": (
                    100.0 * covered_statements / statements if statements else 100.0
                ),
                "covered_branches": covered_branches,
                "branches": branches,
                "branch_percent": (
                    100.0 * covered_branches / branches if branches else 100.0
                ),
            }
    raise RuntimeError(f"Coverage report does not contain {target.file}")


def coverage_for(test_items, target):
    with tempfile.TemporaryDirectory(prefix="ktester-python-coverage-") as temp_dir:
        temp_path = Path(temp_dir)
        report_path = temp_path / "coverage.json"
        result = run_pytest(
            [
                *[str(item) for item in test_items],
                f"--cov={target.module}",
                "--cov-branch",
                f"--cov-report=json:{report_path}",
                "--cov-report=",
                "-q",
            ],
            coverage_file=temp_path / ".coverage",
        )
        if not report_path.exists():
            return None, result.stdout + result.stderr
        return target_coverage(report_path, target), result.stdout + result.stderr


def evaluate_file(test_file, strategy, target):
    collected, nodeids, collection_output = collect_nodeids(test_file)
    result = {
        "strategy": strategy,
        "file": str(test_file),
        "collection_success": collected,
        "collection_output": collection_output,
        "collected_tests": len(nodeids),
    }
    if not collected:
        result.update(
            {
                "passing_tests": 0,
                "epr_percent": None,
                "method_results": [],
                "raw_coverage": None,
                "correct_coverage": None,
            }
        )
        return result

    methods = test_method_results(nodeids)
    passing = [item["nodeid"] for item in methods if item["passed"]]
    raw_coverage, raw_output = coverage_for([test_file], target)
    if passing:
        correct_coverage, correct_output = coverage_for(passing, target)
    else:
        correct_coverage = {
            "covered_statements": 0,
            "statements": raw_coverage["statements"],
            "statement_percent": 0.0,
            "covered_branches": 0,
            "branches": raw_coverage["branches"],
            "branch_percent": 0.0,
        }
        correct_output = "No passing test methods."

    result.update(
        {
            "passing_tests": len(passing),
            "epr_percent": 100.0 * len(passing) / len(nodeids) if nodeids else 0.0,
            "method_results": methods,
            "raw_coverage": raw_coverage,
            "raw_coverage_output": raw_output,
            "correct_coverage": correct_coverage,
            "correct_coverage_output": correct_output,
        }
    )
    return result


def average(values):
    return sum(values) / len(values) if values else None


def summarize(results):
    summary = {}
    for strategy in ("baseline", "guided"):
        group = [item for item in results if item["strategy"] == strategy]
        collected = [item for item in group if item["collection_success"]]
        total_tests = sum(item["collected_tests"] for item in collected)
        total_passing = sum(item["passing_tests"] for item in collected)
        summary[strategy] = {
            "files": len(group),
            "collection_successes": len(collected),
            "collected_tests": total_tests,
            "passing_tests": total_passing,
            "test_method_epr_percent": (
                100.0 * total_passing / total_tests if total_tests else None
            ),
            "average_raw_statement_percent": average(
                [item["raw_coverage"]["statement_percent"] for item in collected]
            ),
            "average_raw_branch_percent": average(
                [item["raw_coverage"]["branch_percent"] for item in collected]
            ),
            "average_correct_statement_percent": average(
                [item["correct_coverage"]["statement_percent"] for item in collected]
            ),
            "average_correct_branch_percent": average(
                [item["correct_coverage"]["branch_percent"] for item in collected]
            ),
        }
    return summary


def files_for(mode, target):
    if mode == "pilot":
        return [
            ("baseline", target.pilot_directory / "baseline.py"),
            ("guided", target.pilot_directory / "guided.py"),
        ]
    files = []
    for strategy in ("baseline", "guided"):
        directory = target.repetitions_directory / strategy
        files.extend((strategy, path) for path in sorted(directory.glob("run_*.py")))
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="generate_manifest_template")
    parser.add_argument("--mode", choices=("pilot", "repetitions"), default="repetitions")
    parser.add_argument("--output")
    args = parser.parse_args()
    target = get_target(args.target)
    selected_files = files_for(args.mode, target)
    if not selected_files:
        raise SystemExit("No generated test files found.")

    results = []
    for strategy, test_file in selected_files:
        print(f"Evaluating {strategy}: {test_file}")
        results.append(evaluate_file(test_file, strategy, target))

    report = {
        "target": target.name,
        "module": target.module,
        "function": target.function,
        "mode": args.mode,
        "python": sys.executable,
        "summary": summarize(results),
        "results": results,
    }
    output_path = Path(args.output) if args.output else (
        target.pilot_directory / "evaluation.json"
        if args.mode == "pilot"
        else target.repetitions_directory / "evaluation.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
