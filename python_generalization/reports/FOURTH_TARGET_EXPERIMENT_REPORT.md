# Fourth Python target experiment: `humanfriendly.parse_size`

## Experimental controls

- Upstream project: `xolox/python-humanfriendly`
- Stable version: `10.0`
- Commit: `6758ac61f906cd8528682003070a57febe4ad3cf`
- Focal function: `parse_size(size, binary=False)` from `humanfriendly/__init__.py`
- Frozen snapshot: `target_functions/parse_size_target.py`
- Model: `openai/gpt-4o-mini-2024-07-18`
- Temperature: `0.5`
- No target-specific prompt optimization was made.
- Generated tests were evaluated exactly as returned; none was manually repaired.
- EPR is measured at pytest test-method granularity.

Frozen prompt SHA-256 values remained unchanged:

| Prompt | SHA-256 |
|---|---|
| `baseline.txt` | `bade34d4723325082a0cf977905584e23a86feb98df5482bba624a8266c47686` |
| `stage1_knowledge.txt` | `031532da7efe99ab7f5bd309a3eef8aef13d99009ef38ab1934e3bbc13240a69` |
| `stage2_scenarios.txt` | `cc8bdda0bbfa7e28d1929b8c13293711c27e463139afb49271ac68909fea96cc` |
| `stage3_generate_test.txt` | `f802272c6634da8792c523060896ce809b44b4ee2db1e508b9f9f3194ac19c5e` |

## Snapshot and dependency control

The stable `10.0` tag and current `master` both resolved to commit
`6758ac61f906cd8528682003070a57febe4ad3cf` on 2026-08-27. The exact upstream
`__init__.py`, `text.py`, `compat.py`, `tests.py`, and MIT license are archived under
`target_functions/provenance/parse_size/upstream/`.

The focal function was copied verbatim. Its canonical AST equals the upstream AST and
has SHA-256 `593796b528b9a2932fc34a7f96d36de034a69087d83e9f40f9697c48fa66868d`.
The snapshot embeds only deterministic constants/helpers: unit named tuples,
`disk_size_units`, `tokenize`, `format`, `is_string`, and `InvalidSize`. Their mapping
and source hashes are recorded in `target_functions/parse_size_PROVENANCE.md`.

Coverage uses coverage.py's function-level summary for `parse_size`, not the module
summary. The reported focal denominator is 14 statements and 12 branches. Statements
and branches in embedded helpers or module-level constants are excluded.

## Contract verification

The Target 4 contract suite checks AST identity plus number-only, bytes, decimal and
binary ambiguous units, explicit IEC units, plurals, fractional values, permissive prefix
matching, and invalid inputs. All 18 Target 4 checks passed. Together with the existing
Target 3 contract checks, the pre-run verification was 21/21 passed.

One initially assumed invalid input, `"1 KB extra"`, exposed an upstream semantic detail:
because ambiguous units use first-letter prefix matching, this input is accepted as KB.
The contract was corrected to record upstream behavior; the focal function was not changed.

## Pilot

| Strategy | Collection | Passed methods | EPR | Raw stmt/branch | Correct stmt/branch |
|---|---:|---:|---:|---:|---:|
| Baseline | 1/1 | 3/4 | 75.00% | 100.00% / 91.67% | 85.71% / 75.00% |
| Guided | 1/1 | 14/16 | 87.50% | 92.86% / 91.67% | 92.86% / 91.67% |

The pilot confirmed generation, collection, test-method EPR, raw focal coverage, and
passing-method-only focal coverage before the formal repetitions started.

## Formal 5x5 results

| Run | Baseline pass | Baseline raw stmt/branch | Baseline correct stmt/branch | Guided pass | Guided raw stmt/branch | Guided correct stmt/branch |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1/3 | 85.71% / 75.00% | 85.71% / 75.00% | 13/15 | 100.00% / 91.67% | 100.00% / 91.67% |
| 2 | 9/10 | 85.71% / 75.00% | 85.71% / 75.00% | 8/15 | 85.71% / 75.00% | 85.71% / 75.00% |
| 3 | 2/3 | 85.71% / 75.00% | 85.71% / 75.00% | 10/14 | 85.71% / 75.00% | 85.71% / 75.00% |
| 4 | 4/7 | 85.71% / 75.00% | 85.71% / 75.00% | 9/12 | 85.71% / 75.00% | 85.71% / 75.00% |
| 5 | 4/5 | 85.71% / 75.00% | 85.71% / 75.00% | 9/15 | 78.57% / 66.67% | 78.57% / 66.67% |

Aggregate metrics:

| Metric | Baseline | Guided |
|---|---:|---:|
| Collection success | 5/5 | 5/5 |
| Test-method EPR | **71.43% (20/28)** | 69.01% (49/71) |
| Average raw statement coverage | 85.71% | **87.14%** |
| Average raw branch coverage | 75.00% | **76.67%** |
| Average correct statement coverage | 85.71% | **87.14%** |
| Average correct branch coverage | 75.00% | **76.67%** |

Unlike Target 3, coverage did not saturate. Formal statement coverage ranged from 78.57%
to 100%, and branch coverage ranged from 66.67% to 91.67%. Neither strategy reached 100%
average raw or correct coverage, so Target 4 adds structural discrimination.

## Local semantic understanding

- `binary=False/True` and `KB` versus `KiB` were generally understood. Both strategies
  repeatedly produced correct decimal KB, binary-flag KB, and explicit KiB/GiB assertions.
  The main exceptions were one Baseline binary-PB multiplier error and two Guided run-2
  MB magnitude errors.
- Number-only inputs were usually handled correctly, including zero and ordinary integers.
  Two Baseline files contain a latent incorrect expectation that `"1.5"` is invalid;
  those assertions were not reached because the same test methods failed earlier while
  resolving an invalid exception reference.
- Singular/plural handling was correctly tested in the executed assertions.
- Prefix matching was incompletely understood. Guided run 1 expected `"1 KB KB"` to be
  rejected, but the source accepts it because the whole unit token starts with `k`.
- Invalid-unit behavior was usually described correctly, but many final tests referenced
  `parse_size.InvalidSize` or an unimported `InvalidSize`, so they failed before exercising
  the intended call. This is test-construction failure, not evidence of a wrong source oracle.

## Failure and oracle analysis

Thirty formal test methods failed: 8 Baseline and 22 Guided.

Baseline failures:

- 5 construction failures: two used `parse_size.InvalidSize`; three used an unimported
  `InvalidSize` despite the frozen prompt's exact target import.
- 3 numeric-oracle failures: the binary 1.5 PB value was too small, one method shifted
  PB/EB/ZB/YB decimal magnitudes down by three orders, and another undercounted 0.1 PB.
- Additional latent oracles inside already-failing exception methods treated number-only
  `"1.5"`, valid ZB, or permissively prefixed `"1.5 GB invalid"` as invalid.

Guided failures:

- 14 construction failures used `parse_size.InvalidSize`. Most associated scenarios had
  the right high-level expectation, but the final test could not resolve the exception.
- 5 methods undercounted `1 YB` as `10^18` instead of `10^24`.
- 2 methods overcounted `1.5 MB` by a factor of 1000 in decimal and binary modes.
- 1 method expected the permissive prefix input `"1 KB KB"` to raise.
- The run-2 `None` scenario also had a latent type-oracle error: `tokenize(None)` raises
  `TypeError`, not `InvalidSize`, but Stage 3 failed earlier resolving the exception object.

Raw and correct coverage are equal in every formal run. This does not mean every oracle
was correct: the failing methods' covered branches were redundant with passing methods, so
removing failures did not reduce structural coverage.

## Intermediate-error propagation

All eight Guided semantic-oracle failures were already specified in Stage 2 and then
implemented in Stage 3: five wrong YB expectations, two wrong MB expectations, and the
wrong duplicate-unit expectation. Stage 1 was usually generic about large or malformed
inputs; Stage 2 introduced the precise incorrect expected values or behavior.

The 14 `parse_size.InvalidSize` failures are a different propagation pattern. Stage 2
correctly named the exception for most invalid-string scenarios, but Stage 3 converted
that name into an invalid attribute access because only the focal function was imported.
Thus Guided exhibited both intermediate semantic error propagation and final-stage test
construction error.

## Trend across four targets

- `parse_bindings`: Baseline EPR 80.00%; Guided EPR 86.11% among four collecting runs,
  with one additional Guided collection failure. Correct coverage was effectively 80%
  across five runs when that unusable run was counted as zero.
- `is_main_conference`: Baseline EPR 65.00%; Guided EPR 60.00%. Raw coverage tied at
  94.12% statements / 90.00% branches; correct coverage was close, with a small Guided
  branch advantage.
- `generate_manifest_template`: Baseline EPR 100.00%; Guided EPR 84.21%; all raw and
  correct coverage metrics saturated at 100%.
- `parse_size`: Baseline EPR 71.43%; Guided EPR 69.01%. Guided has a small coverage edge
  (about 1.43 statement points and 1.67 branch points) but lower EPR and many more failed
  methods. Importantly, it avoids coverage saturation.

Across four targets there is still no consistent evidence that the Guided pipeline improves
overall generated-test quality. It tends to produce more test methods and occasionally more
coverage, but intermediate numerical/semantic errors and final-stage exception construction
can offset that exploration.

## Artifacts and final integrity

- Pilot: `generated_tests/pilots/parse_size/`
- Formal 5x5 tests and all ten Guided Stage 1/2 files:
  `generated_tests/repetitions/parse_size/`
- Machine-readable evaluation: `generated_tests/repetitions/parse_size/evaluation.json`
- Snapshot provenance: `target_functions/parse_size_PROVENANCE.md`
- Archived upstream evidence: `target_functions/provenance/parse_size/upstream/`
- Contract tests: `tests/test_parse_size_target.py`
- Pre-change backup: `target4_prechange_20260827/`

Final verification confirmed 5 Baseline test files, 5 Guided test files, 5 Stage 1 files,
5 Stage 2 files, unchanged prompt hashes, snapshot/upstream AST identity, focal-only coverage,
and successful collection of all ten formal test files. File-level hashes are recorded in
`generated_tests/repetitions/parse_size/artifact_manifest.sha256`.
