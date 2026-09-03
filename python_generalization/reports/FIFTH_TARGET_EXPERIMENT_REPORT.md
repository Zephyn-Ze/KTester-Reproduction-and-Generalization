# Fifth Python target experiment: `black.normalize_string_quotes`

## Candidate screening

Four mature-project candidates were screened before the target was frozen:

| Candidate | Shape | Decision |
|---|---|---|
| Black `normalize_string_quotes` | 71-line pure string-rule function; branches over quote kind, raw/f prefixes, escapes, regex matches, and triple quotes | Selected |
| Click `_unpack_args` | Compact collection unpacker with forward/reverse traversal and wildcard nargs | Rejected because it is shorter and its most distinctive behavior depends on Click's private `UNSET` sentinel |
| HTTPX `get_environment_proxies` | Multi-branch URL/domain/IP normalization | Rejected because it reads environment and system proxy configuration |
| Packaging tag/platform helpers | Non-trivial tag and platform rules | Rejected because the useful candidates couple to internal platform/type helpers and runtime platform detection |

Black was selected because it differs materially from Target 4's unit parsing while retaining
non-obvious local semantics and a minimal standard-library-only snapshot. A few tests do not
trivially cover the raw-string, f-string, triple-quote, escape-removal, escape-increase, and
double-quote tie-breaking branches.

## Experimental controls

- Upstream project: `psf/black`
- Stable version: `26.5.1`
- Commit: `87928e6d6761a4a6d22250e1fee5601b3998086e`
- Upstream path: `src/black/strings.py`, lines 169-239
- License: MIT
- Focal function: `normalize_string_quotes(s: str) -> str`
- Frozen snapshot: `target_functions/normalize_string_quotes_target.py`
- Model: `openai/gpt-4o-mini-2024-07-18`
- Temperature: `0.5`
- No target-specific prompt optimization was made.
- Generated tests were evaluated exactly as returned; none was manually repaired.
- EPR is measured at pytest test-method granularity among files that collect.

Frozen prompt SHA-256 values remained unchanged:

| Prompt | SHA-256 |
|---|---|
| `baseline.txt` | `bade34d4723325082a0cf977905584e23a86feb98df5482bba624a8266c47686` |
| `stage1_knowledge.txt` | `031532da7efe99ab7f5bd309a3eef8aef13d99009ef38ab1934e3bbc13240a69` |
| `stage2_scenarios.txt` | `cc8bdda0bbfa7e28d1929b8c13293711c27e463139afb49271ac68909fea96cc` |
| `stage3_generate_test.txt` | `f802272c6634da8792c523060896ce809b44b4ee2db1e508b9f9f3194ac19c5e` |

## Snapshot and provenance

The official tagged `strings.py` and MIT license are archived under
`target_functions/provenance/normalize_string_quotes/upstream/`. The focal function is
copied verbatim. Its canonical AST equals the upstream AST and has SHA-256
`06d48905c38db6cf534e7c8eca0656a96055714613c994d43b9e446ed98059de`.

The snapshot embeds only the exact `STRING_PREFIX_CHARS` value and the deterministic
`sub_twice` and `_cached_compile` helpers. It uses only `re`, `functools`, and typing
imports. Detailed file hashes and helper mappings are in
`target_functions/normalize_string_quotes_PROVENANCE.md`.

Coverage uses coverage.py's function summary for `normalize_string_quotes`, not module
coverage. The focal denominator is 42 statements and 24 branches; helper statements and
module-level setup are excluded.

## Contract verification

The contract suite checks AST identity and 18 behavioral cases: ordinary single/double
quotes, bytes and raw prefixes, triple quotes, removable escapes, quote conversion that
would add escapes, raw strings, f-strings, empty input, and malformed quote-free input.
All 19 pytest items passed, including the AST check.

Important local semantics recorded by the contracts include:

- ordinary single quotes convert to double quotes when escaping does not increase;
- existing double quotes win a tie and remain double quoted;
- triple single quotes convert to triple double quotes;
- raw-string content does not have escapes added or removed;
- the input is the textual representation of a Python string token, including prefix and
  delimiters, not the runtime value of that token;
- empty input raises `IndexError`; a non-empty quote-free input reaches the focal
  `AssertionError`.

## Pilot

| Strategy | Collection | Passed methods | EPR | Raw stmt/branch | Correct stmt/branch |
|---|---:|---:|---:|---:|---:|
| Baseline | 0/1 | 0/0 | N/A | N/A | N/A |
| Guided | 1/1 | 3/12 | 25.00% | 69.05% / 50.00% | 66.67% / 45.83% |

The Baseline pilot contained an invalid generated f-string and failed during collection.
This was retained as a test-construction failure. Guided generation, Stage 1/2 persistence,
collection, method-level EPR, and focal-only raw/correct coverage all operated correctly,
so the formal repetitions proceeded without repairing either pilot file.

## Formal 5x5 results

| Run | Baseline pass | Baseline raw stmt/branch | Baseline correct stmt/branch | Guided pass | Guided raw stmt/branch | Guided correct stmt/branch |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | collection failed | N/A | N/A | 3/10 | 78.57% / 62.50% | 66.67% / 45.83% |
| 2 | collection failed | N/A | N/A | 5/10 | 78.57% / 66.67% | 71.43% / 54.17% |
| 3 | 0/3 | 69.05% / 50.00% | 0.00% / 0.00% | collection failed | N/A | N/A |
| 4 | collection failed | N/A | N/A | 5/12 | 80.95% / 70.83% | 76.19% / 66.67% |
| 5 | collection failed | N/A | N/A | 4/11 | 69.05% / 50.00% | 69.05% / 50.00% |

Primary evaluator summary (coverage averages are over collecting files only):

| Metric | Baseline | Guided |
|---|---:|---:|
| Collection success | 1/5 | **4/5** |
| Test-method EPR among collecting files | 0.00% (0/3) | **39.53% (17/43)** |
| Average raw statement coverage | 69.05% | **76.79%** |
| Average raw branch coverage | 50.00% | **62.50%** |
| Average correct statement coverage | 0.00% | **70.83%** |
| Average correct branch coverage | 0.00% | **54.17%** |

Because collection rates differ sharply, the table above must not be read as equal-sample
coverage. Counting every non-collecting run as zero gives these all-five-run descriptive
means:

| Metric | Baseline | Guided |
|---|---:|---:|
| Effective raw statement | 13.81% | 61.43% |
| Effective raw branch | 10.00% | 50.00% |
| Effective correct statement | 0.00% | 56.67% |
| Effective correct branch | 0.00% | 43.33% |

Target 5 avoids coverage saturation, but its main discrimination is generated-test
executability and semantic reliability rather than a small coverage difference.

## Failure classification

### Collection and construction failures

Five formal files failed collection:

- Baseline runs 1, 2, 4, and 5 contain invalid or unterminated Python string literals
  caused by incorrect quote/backslash construction.
- Guided run 3 contains an invalid quote-heavy assertion and fails with `SyntaxError`.

These are final-test construction failures. They are not source-function exceptions and
contribute no methods to EPR or coverage.

The one collecting Baseline file contains three test methods and all three fail. Each method
stops at an early wrong quote-conversion oracle, so later assertions in those methods are
not independently counted by method-level EPR.

### Guided method failures

Across the four collecting Guided files, 26 of 43 methods fail. Manual classification of
the first failing assertion in each method gives:

- 19 semantic/oracle failures: converting already preferred double quotes to single quotes,
  preserving triple single quotes, treating empty or quote-free inputs as unchanged,
  preserving single-quoted f tokens, incorrect escape-count expectations, or otherwise
  expecting a quote conversion that the focal rules reject.
- 7 input-construction/representation failures: a Python raw/f literal was used to build
  the test input, but evaluation removed the literal's `r`/`f` prefix and delimiter
  characters. The focal function therefore received a runtime value rather than the
  textual token representation its caller supplies.

There are no import failures or wrong exception-object references in Target 5. Exception
errors are semantic: generated tests expect empty or quote-free inputs to be returned
unchanged even though the implementation raises `IndexError` or `AssertionError`.

## Intermediate-error propagation

All 26 failing Guided methods have a corresponding incorrect expected behavior or
incorrect input representation in Stage 2, which Stage 3 implements. Repeated propagated
errors include:

- “double quotes convert to single quotes” despite the explicit tie-break that prefers
  existing double quotes;
- “triple single quotes remain unchanged” instead of conversion to triple double quotes;
- empty and quote-free inputs return unchanged;
- raw/f Python literals are passed as if their runtime values still contain the prefix and
  outer delimiters;
- raw and formatted string tokens remain unchanged even when safe conversion to double
  quotes is required.

Stage 1 often states the high-level “prefer double quotes” rule and notices the assertion
for missing quotes, but Stage 2 frequently contradicts that knowledge with concrete wrong
oracles. Stage 1 run 4 also incorrectly generalizes that all triple-quoted strings remain
unchanged. The Guided run-3 syntax error becomes executable only in Stage 3, although its
quote-heavy scenario text was already ambiguous in Stage 2.

Thus Target 5 demonstrates both intermediate semantic-error propagation and final-stage
syntax construction failure.

## Unified trend across five targets

| Target | Baseline EPR | Guided EPR | Main result |
|---|---:|---:|---|
| `parse_bindings` | 80.00% | 86.11% among four collecting runs | Small Guided EPR edge, but one Guided collection failure; effective correct coverage tied at 80% when that run is zero |
| `is_main_conference` | 65.00% | 60.00% | Baseline EPR higher; raw coverage tied, correct coverage nearly tied |
| `generate_manifest_template` | 100.00% | 84.21% | Baseline EPR higher; all coverage saturated |
| `parse_size` | 71.43% | 69.01% | Baseline EPR higher; Guided has only a small coverage edge |
| `normalize_string_quotes` | 0.00% among one collecting run | 39.53% among four collecting runs | Guided is clearly more executable and covers more, but absolute EPR remains low |

Target 5 is the strongest relative Guided win, primarily because Baseline collapses on
quote-heavy Python syntax. It does not establish reliable Guided test quality: Guided still
has one collection failure and 26 failing methods, and most semantic errors are already
present in Stage 2.

Across five targets, Guided wins nominal EPR on two targets and loses on three. Its coverage
advantage is inconsistent, sometimes absent or saturated, and can coexist with low EPR.
The five-target evidence therefore does **not** support the claim that the current
knowledge-guided Python pipeline is stably superior to direct Baseline generation. It
supports a narrower claim: intermediate guidance can improve exploration or executability
for some targets, but it also propagates invented or misread local semantics and does not
reliably improve overall generated-test correctness.

## Artifacts

- Pilot: `generated_tests/pilots/normalize_string_quotes/`
- Formal 5x5 tests and all Guided Stage 1/2 files:
  `generated_tests/repetitions/normalize_string_quotes/`
- Machine-readable evaluation:
  `generated_tests/repetitions/normalize_string_quotes/evaluation.json`
- Snapshot: `target_functions/normalize_string_quotes_target.py`
- Provenance: `target_functions/normalize_string_quotes_PROVENANCE.md`
- Archived upstream evidence:
  `target_functions/provenance/normalize_string_quotes/upstream/`
- Contract tests: `tests/test_normalize_string_quotes_target.py`
- Integrity manifest:
  `generated_tests/repetitions/normalize_string_quotes/artifact_manifest.sha256`

