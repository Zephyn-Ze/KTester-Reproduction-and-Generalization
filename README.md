# KTester Reproduction and Lightweight Python Generalization

This repository documents an independent **reproduction, diagnosis, and lightweight Python generalization study** of KTester, the ICSE 2026 paper *Knowledge Matters: Injecting Project and Testing Knowledge into LLM-based Unit Test Generation*.

It is not an official KTester repository, a reimplementation of the complete KTester system, or a complete Python port. The goal is narrower: preserve auditable local results, explain why one 111-focal-method run differed from the paper, test repair-related hypotheses under controlled conditions, and probe whether a small knowledge-guided workflow generalizes to five Python functions.

## Main findings

### Java reproduction and diagnosis

The local run evaluated 111 focal methods with `openai/gpt-4o-mini-2024-07-18` at temperature `0.5`. Its aggregate values were lower than the paper's Table 2 results:

| Source | CPR | EPR | IC | BC | Correct IC | Correct BC |
|---|---:|---:|---:|---:|---:|---:|
| Paper Table 2 | 100.00% | 76.41% | 63.94% | 55.46% | 55.52% | 47.21% |
| Local Run3, 111 focal methods | 90.09% | 53.74% | 49.90% | 44.85% | 40.79% | 36.09% |

The evidence supports degraded generation/repair quality as the strongest near-term explanation. Prompt/context drift, provider/backend details, and exact historical artifact provenance remain unresolved. The repository therefore does **not** claim a successful exact reproduction of Table 2.

### Controlled repair comparison

A paired three-case intervention reused identical initial generated tests and varied only repair information:

| Condition | CPR | KTester-filtered EPR | Raw JUnit EPR | Correct IC | Correct BC |
|---|---:|---:|---:|---:|---:|
| Current repair | 66.67% | 17.65% | 5.88% | 32.33% | 31.00% |
| Enhanced repair | 100.00% | 61.54% | 38.46% | 44.00% | 43.00% |
| Enhanced repair + focal source | 100.00% | 66.67% | 46.67% | 48.67% | 47.67% |

These are deliberately selected failure cases, not an unbiased 111-case estimate. A separate 12-case, three-repetition experiment found substantial stochasticity, but even its best repetition remained below the corresponding official artifacts.

### Five Python targets

The Python study compares direct Baseline generation with a three-stage Guided flow: knowledge extraction, scenario design, and test generation.

| Target | Baseline EPR | Guided EPR | Main observation |
|---|---:|---:|---|
| `parse_bindings` | 80.00% | 86.11% among four collecting runs | Small Guided EPR edge; one Guided collection failure |
| `is_main_conference` | 65.00% | 60.00% | Baseline higher; coverage nearly tied |
| `generate_manifest_template` | 100.00% | 84.21% | Coverage saturated at 100% for both |
| `parse_size` | 71.43% | 69.01% | Baseline slightly higher; Guided coverage edge was small |
| `normalize_string_quotes` | 0.00% among one collecting run | 39.53% among four collecting runs | Guided was more executable, but absolute correctness remained low |

Across these five functions, Guided wins nominal EPR on two targets and loses on three. The evidence supports a limited conclusion: intermediate guidance can improve exploration or executability on some targets, but can also propagate invented or misunderstood semantics.

## Metric definitions and caveats

- **CPR**: proportion of focal-method artifacts whose generated test class compiled.
- **EPR**: passed generated test methods divided by generated test methods. It is not the proportion of completely passing classes.
- **IC/BC**: instruction and branch coverage as emitted by the local JaCoCo-based evaluator. The paper labels the first coverage column as line coverage; this repository preserves the evaluator's operational `instruction_coverage` name.
- **Correct coverage**: focal coverage attributable to passing generated test methods.
- Python EPR is computed at pytest test-method granularity. Coverage averages in the Python reports are over files that collected unless an all-run effective metric is explicitly shown.
- A syntax/import/collection failure contributes no test methods to the collecting-only EPR denominator. Collection rates must therefore be reported alongside EPR.
- High raw coverage is not proof of correct oracles or even correct focal binding.

## Repository map

```text
.
├── reproduction/
│   ├── reports/             # public, path-sanitized diagnosis
│   └── results/             # the 111-focal-method local summary
├── repair_analysis/
│   ├── reports/             # paired repair and stochasticity reports
│   └── results/             # compact CSV/JSON evidence
├── python_generalization/
│   ├── reports/             # target-specific experiment reports
│   ├── prompts/             # frozen prompt templates
│   ├── generated_tests/     # model outputs, Stage 1/2 artifacts, evaluations
│   ├── target_functions/    # frozen focal snapshots and provenance
│   └── tests/               # snapshot/contract checks
├── tables/                  # compact headline tables
├── figures/                 # figure policy and future exports
├── LICENSES/                # third-party MIT license texts
├── PROVENANCE.md
└── MANIFEST.sha256
```

## Reusing the Python artifacts

The preserved environment used Python `3.13.14`, `openai==2.6.1`, `pytest==9.1.1`, `coverage==7.15.4`, and `pytest-cov==7.1.0`. The model and temperature are frozen in `python_generalization/llm/config.py`; the API key is read only from the `OPENROUTER_API_KEY` environment variable and is never stored here.

Install the dependencies and run contract checks from `python_generalization/`:

```bash
python -m pip install -r requirements.txt
python -m pytest tests
```

Existing generated outputs should be treated as immutable evidence. If generating new runs, write to a new directory and record the provider, model string, temperature, prompt hashes, timestamp, collection denominator, and focal-only raw/correct coverage.

## Source and licensing boundary

The upstream KTester checkout did not contain a license file when this package was prepared, so this repository deliberately excludes the upstream KTester implementation, prompt templates, Java dependency bundles, dataset projects, and official evaluation archive. It links to the upstream repository and includes only independently created analysis plus locally generated compact results.

The `parse_size` and `normalize_string_quotes` snapshots are derived from MIT-licensed projects, with exact source identity and license copies retained. See [PROVENANCE.md](PROVENANCE.md) and [LICENSES](LICENSES/).

No blanket open-source license is granted for this repository's original material at this time. See [LICENSE.md](LICENSE.md).

## References

- [KTester official repository](https://github.com/SYSUSELab/KTester)
- [KTester preprint](https://arxiv.org/abs/2511.14224)
- [Black](https://github.com/psf/black)
- [python-humanfriendly](https://github.com/xolox/python-humanfriendly)

