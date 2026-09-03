# Local Run3 versus KTester Table 2

## Scope

This is a public, path-sanitized summary of a read-only diagnosis. The local KTester checkout and its evaluation artifacts were not modified during the diagnosis.

## Aggregate comparison

| Source | CPR | EPR | IC | BC | Correct IC | Correct BC |
|---|---:|---:|---:|---:|---:|---:|
| Paper Table 2 | 100.00% | 76.41% | 63.94% | 55.46% | 55.52% | 47.21% |
| Local Run3 | 90.09% | 53.74% | 49.90% | 44.85% | 40.79% | 36.09% |
| Difference, local minus paper | -9.91 pp | -22.67 pp | -14.04 pp | -10.61 pp | -14.73 pp | -11.12 pp |

The local JSON contains 111 focal-method records plus the aggregate fields. Only 9 of the 111 generated test classes were completely passing, while the evaluator's EPR is a method-level passed-test ratio. These are different quantities and should not be conflated.

## Strongly supported cause

Generated and repaired test quality is the strongest demonstrated near-cause. The local run began with substantially more compilation failures than one official repetition and retained final compilation failures that the released official repetitions did not. Concrete failure modes included hallucinated APIs, inaccessible types or constructors, undefined variables, generic clashes, wrong assertions, timeouts, and nominally passing tests with no production focal coverage.

The controlled repair comparison strengthens the causal claim: keeping the initial generated tests fixed while improving repair diagnostics/context raised CPR, both EPR variants, and correct coverage on selected failure cases.

## What is not established

- Exact historical prompt/context identity between the local run and every official repetition.
- Exact provider/backend snapshot despite a matching model string.
- A single, byte-reproducible provenance chain for every released official final test.
- That randomness alone explains the gap. The 12-case repetitions show large variability, but all three remain below the corresponding official artifacts.

## Metric caveat

The evaluator field is JaCoCo instruction coverage even though the paper labels the first coverage metric as line coverage. Direct spot checks showed that this naming difference is too small to explain the observed aggregate gap, but the operational field name is retained here as IC.

