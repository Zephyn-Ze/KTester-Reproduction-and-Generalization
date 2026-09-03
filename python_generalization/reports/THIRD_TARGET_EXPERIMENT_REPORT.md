# Third Python target experiment: `generate_manifest_template`

## Experimental controls

- Target source: user-supplied `inventory.py`, function `generate_manifest_template`
- Frozen snapshot: `target_functions/generate_manifest_template_target.py`
- Model: `openai/gpt-4o-mini-2024-07-18`
- Temperature: `0.5`
- Baseline and Guided prompts were not semantically changed.
- Generated tests were executed as returned by the model and were not manually repaired.
- EPR is measured at pytest test-method granularity. A method may contain multiple assertions.

Frozen prompt SHA-256 values:

| Prompt | SHA-256 |
|---|---|
| `baseline.txt` | `bade34d4723325082a0cf977905584e23a86feb98df5482bba624a8266c47686` |
| `stage1_knowledge.txt` | `031532da7efe99ab7f5bd309a3eef8aef13d99009ef38ab1934e3bbc13240a69` |
| `stage2_scenarios.txt` | `cc8bdda0bbfa7e28d1929b8c13293711c27e463139afb49271ac68909fea96cc` |
| `stage3_generate_test.txt` | `f802272c6634da8792c523060896ce809b44b4ee2db1e508b9f9f3194ac19c5e` |

The only structural prompt substitution remains target file/module/function information.
`experiment_targets.py` now supplies these values for all three targets. Generation and
evaluation scripts accept `--target`, so later targets do not require repeated hard-coded
path edits. Guided Stage 1 and Stage 2 responses are now saved alongside each final test.

## Why this target was selected

`generate_manifest_template` is a standalone pure data transformation with iteration,
year grouping, two record-shape branches, field remapping, and journal display-name
construction. It has no network, file-system, plotting, or third-party runtime dependency.

`extract_method_from_title` was considered but rejected because its helper depends on NLTK
and the WordNet corpus, neither of which is available in the experiment interpreter. Adding
them would confound generated-test quality with external resource availability.

## Pilot

| Strategy | Collection | Passed methods | EPR | Raw stmt/branch | Correct stmt/branch |
|---|---:|---:|---:|---:|---:|
| Baseline | 1/1 | 6/6 | 100% | 100% / 100% | 100% / 100% |
| Guided | 1/1 | 10/10 | 100% | 100% / 100% | 100% / 100% |

The pilot verified the complete generation, collection, EPR, raw coverage, and correct
coverage path before the repetitions were started.

## Formal 5x5 results

| Run | Baseline pass | Baseline raw stmt/branch | Baseline correct stmt/branch | Guided pass | Guided raw stmt/branch | Guided correct stmt/branch |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5/5 | 100% / 100% | 100% / 100% | 5/6 | 100% / 100% | 100% / 100% |
| 2 | 5/5 | 100% / 100% | 100% / 100% | 5/6 | 100% / 100% | 100% / 100% |
| 3 | 5/5 | 100% / 100% | 100% / 100% | 7/8 | 100% / 100% | 100% / 100% |
| 4 | 2/2 | 100% / 100% | 100% / 100% | 9/10 | 100% / 100% | 100% / 100% |
| 5 | 5/5 | 100% / 100% | 100% / 100% | 6/8 | 100% / 100% | 100% / 100% |

Aggregate metrics:

| Metric | Baseline | Guided |
|---|---:|---:|
| Collection success | 5/5 | 5/5 |
| Test-method EPR | **100.00% (22/22)** | 84.21% (32/38) |
| Average raw statement coverage | 100% | 100% |
| Average raw branch coverage | 100% | 100% |
| Average correct statement coverage | 100% | 100% |
| Average correct branch coverage | 100% | 100% |

## Guided failure and oracle analysis

Six Guided methods failed; no Baseline method failed.

1. Unsupported `kind` semantics (three methods):
   - `test_unexpected_kind_value` expected an unknown kind to be ignored, but the source's
     `else` branch attempted to read journal fields and raised `KeyError`.
   - `test_invalid_kind_value` expected the original invalid kind in the output, but the
     source emitted the literal output kind `journal`.
   - `test_record_with_invalid_kind` expected the record to be ignored, but the source's
     `else` branch attempted journal-field access and raised `KeyError`.
2. Invented year validation (one method): `test_invalid_year_format` expected `KeyError`
   for `"2023a"`; the source accepts it unchanged as a dictionary key.
3. Invented type validation (one method): `test_incorrect_data_types` expected `TypeError`
   for a string `paper_count`; the source only copies that value.
4. Invented missing-field recovery (one method):
   `test_record_with_missing_required_fields` expected partial processing and a `"None"`
   display name; direct source indexing instead raises `KeyError`.

The dominant error mechanism is Guided intermediate reasoning introducing validation or
recovery behavior that the source does not implement. The incorrect expectations are
already present in Stage 2 for the invalid-year, incorrect-type, missing-field, and most
invalid-kind scenarios, and Stage 3 implements them faithfully. This is evidence of
intermediate-error propagation, not evidence that the source should be changed.

## Comparison with the first two targets

- `parse_bindings`: Baseline EPR was 80.00% (20/25). Guided EPR was 86.11% (31/36)
  among four collecting runs, with one additional Guided file failing collection. Mean
  correct coverage across all five runs was 80% for both strategies when the non-usable
  run was counted as zero. Coverage saturated because the target had 13 statements and
  8 branches.
- `is_main_conference`: Baseline EPR was 65.00% (13/20), Guided EPR was 60.00% (30/50).
  Both averaged 94.12% raw statement and 90.00% raw branch coverage. Correct statement
  coverage tied at 90.59%; Guided correct branch coverage was 86.00% versus Baseline
  84.00%. Its main semantic failure was misunderstanding `ASE -> kbse` and
  `FSE -> sigsoft`.
- `generate_manifest_template`: Baseline dominates EPR (100.00% versus 84.21%), while
  raw and correct coverage are tied at 100%. Guided explores more malformed-input and
  validation scenarios, but those extra scenarios introduce unsupported oracles and do
  not add structural coverage.

Across the three targets, there is not yet evidence that the Guided pipeline provides a
consistent overall improvement. It often creates more independently named scenarios, but
its added reasoning can either omit local source semantics or invent validation behavior.
Raw coverage alone masks these problems because a smaller set of passing tests can already
cover every branch in simple targets.

## Artifacts

- Pilot tests and report: `generated_tests/pilots/generate_manifest_template/`
- 5x5 tests, Guided intermediate artifacts, and detailed evaluation:
  `generated_tests/repetitions/generate_manifest_template/`
- Machine-readable formal report:
  `generated_tests/repetitions/generate_manifest_template/evaluation.json`
- Snapshot provenance: `target_functions/generate_manifest_template_PROVENANCE.md`
