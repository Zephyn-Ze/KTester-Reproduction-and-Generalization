# Provenance and publication boundary

Prepared on 2026-09-03 from preserved local artifacts. The source directories were read and copied selectively; no original file was deleted, renamed, or overwritten.

## Upstream KTester

- Repository: https://github.com/SYSUSELab/KTester
- Local checkout commit: `fce83f1a4b9aa3f1d54598b62027bc17bb585383`
- Local checkout state: modified and mixed with generated/evaluation artifacts; it is not represented as a clean historical snapshot.
- License finding: no `LICENSE`, `COPYING`, or `NOTICE` file was present in the checked commit or visible repository root when this package was prepared.
- Publication decision: do not redistribute the KTester source tree, Java archives, dependency jars, downloaded Maven projects, official evaluation archive, or KTester prompt templates. Link to upstream instead.

`reproduction/results/run3_111_focal_methods.json` is a locally generated evaluator summary for 111 focal methods. The public report and tables were independently written from that result, the paper's Table 2, and read-only diagnostic evidence.

## Repair analysis

The compact reports and result tables under `repair_analysis/` come from isolated local experiments. Large copied worktrees, compiled dependencies, raw API responses, repair logs, generated Java trees, and local settings files were excluded. This keeps the public package focused on the evidence needed to interpret the experiments without redistributing the upstream implementation.

## Python targets

| Target | Origin | Publication treatment |
|---|---|---|
| `parse_bindings` | User's local Python analysis utility | Minimal frozen snapshot retained |
| `is_main_conference` | User's local Python analysis utility | Minimal frozen snapshot retained |
| `generate_manifest_template` | User-supplied `inventory.py`, source SHA-256 recorded in its provenance file | Minimal frozen snapshot retained |
| `parse_size` | `xolox/python-humanfriendly`, tag `10.0`, commit `6758ac61f906cd8528682003070a57febe4ad3cf` | MIT snapshot, upstream evidence, and license retained |
| `normalize_string_quotes` | `psf/black`, release `26.5.1`, commit `87928e6d6761a4a6d22250e1fee5601b3998086e` | MIT snapshot, upstream evidence, and license retained |

The archived upstream Python files are present only to verify focal-function identity and the dependency mapping documented by the contract tests. Their original MIT terms remain in `LICENSES/` and alongside each archived snapshot.

## Generated material

Files under `python_generalization/generated_tests/` are preserved model outputs and evaluation records from the experiment. They were not manually repaired. Guided Stage 1 and Stage 2 outputs remain beside the corresponding final tests where available.

## Frozen prompt hashes

| Prompt | SHA-256 |
|---|---|
| `baseline.txt` | `bade34d4723325082a0cf977905584e23a86feb98df5482bba624a8266c47686` |
| `stage1_knowledge.txt` | `031532da7efe99ab7f5bd309a3eef8aef13d99009ef38ab1934e3bbc13240a69` |
| `stage2_scenarios.txt` | `cc8bdda0bbfa7e28d1929b8c13293711c27e463139afb49271ac68909fea96cc` |
| `stage3_generate_test.txt` | `f802272c6634da8792c523060896ce809b44b4ee2db1e508b9f9f3194ac19c5e` |

`MANIFEST.sha256` records hashes for the final publication package and should be regenerated only when the package intentionally changes.

