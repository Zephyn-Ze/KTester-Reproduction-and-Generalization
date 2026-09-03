# KTester 12-case × 3-repetition stratified experiment

## Bottom line

The experiment rejects the simple claim that Table 2 is high mainly because the authors got a lucky random draw.

LLM stochasticity is material: 5 of 12 cases flipped compile status, 5 of 12 flipped whether all tests passed, and the three-repetition aggregate ranges reached 16.67 percentage points for CPR and 12.25 points for correct branch coverage. Fresh repetitions also substantially outperformed the deliberately failure-heavy Run3 subset.

However, randomness alone does not close the gap. Even the best of the three current-flow repetitions reached only 83.33% CPR and 38.14% EPR, versus 100% and 73.90% for the same 12 cases averaged over the five official repetitions. Three cases were stably ineffective in all new repetitions while the official artifacts compiled and covered them. Combined with the earlier paired enhanced-repair experiment, the strongest supported conclusion is:

1. repair/generation strategy is the strongest verified actionable contributor;
2. LLM stochasticity is the second major contributor and makes a single Run3 unreliable;
3. official prompt/context and possibly provider/backend settings remain an unresolved residual;
4. environment and artifact provenance are not the main causes of Run3's low correct coverage.

## Experimental controls

- Selected 12 cases from jdom2, commons-codec, Gson, and ruler, covering compile failures, API hallucination, wrong oracle/assertion, timeout, runner failure, and low focal coverage.
- Model: `openai/gpt-4o-mini-2024-07-18`; temperature 0.5; `FIX_TRIES=5`; four API workers.
- The three repetitions have identical hashes for settings, open-source repair code, prompt templates, evaluation code, and observational instrumentation.
- Java 17 was used. Production resources were copied from each isolated project's `src/main/resources` into its isolated `target/classes` before execution.
- Both ordinary and verbose test execution used a uniform 15-second safety cap. This only shortens timeout detection. It does not change prompts, generated code, repair prompts, or success criteria.
- All 355 recorded OpenRouter responses reported the requested model. Six system fingerprints occurred in every repetition, so the model name was stable but the requests were not served by one observable fingerprint.
- The preserved local KTester checkout was not modified. Its four key source hashes, tracked-status hash, and Run3 summary modification time remained unchanged.

### Prompt-control nuance

KTester is a two-stage stochastic pipeline. The fixed init/condition/io/exception prompts were identical across the three repetitions. Of 60 saved prompt files (five prompt types × 12 cases), 50 were byte-identical. The ten differences were all `gencode_prompt.md`: upstream sampled test-case descriptions are embedded in the downstream code-generation prompt. This is not an uncontrolled code/config difference; it is the mechanism by which early LLM randomness cascades into later generation.

Therefore, this experiment estimates end-to-end KTester stochasticity under a fixed prompt construction and fixed configuration. It is not a one-shot replay of one byte-identical final gencode prompt.

## Group-meeting table

All values are percentages. EPR is total passed test cases divided by total generated test cases for the selected 12 cases.

| Source | CPR | EPR | IC | BC | Correct IC | Correct BC |
|---|---:|---:|---:|---:|---:|---:|
| Run3 selected baseline | 66.67 | 7.52 | 6.25 | 5.75 | 2.92 | 3.08 |
| New rep 1 | 75.00 | 32.71 | 40.08 | 33.33 | 35.25 | 27.75 |
| New rep 2 | 66.67 | 31.09 | 46.25 | 43.00 | 41.00 | 37.92 |
| New rep 3 | 83.33 | 38.14 | 48.75 | 39.83 | 35.08 | 25.67 |
| New three-rep mean | 75.00 | 33.98 | 45.03 | 38.72 | 37.11 | 30.44 |
| New three-rep range | 16.67 | 7.05 | 8.67 | 9.67 | 5.92 | 12.25 |
| Official five-rep mean, same 12 cases | 100.00 | 73.90 | 61.20 | 50.80 | 50.47 | 41.40 |
| Paper Table 2, all 111 cases | 100.00 | 76.41 | 63.94 | 55.46 | 55.52 | 47.21 |

The 12-case subset was intentionally selected from Run3 failures, so its absolute values must not be compared as an unbiased estimate of all 111 cases. The valid comparisons are within the fixed selected set and the amount of between-repetition variation.

## What the repetitions prove

### Strong stochastic cases

| Case | Correct IC across new reps | Official mean correct IC | Interpretation |
|---|---:|---:|---|
| `Rule_pattern` | 0 / 100 / 0 | 60.0 | One repetition became fully correct; two produced no correct coverage. |
| `Sha2Crypt_sha2Crypt` | 93 / 93 / 0 | 94.0 | Two repairs neutralized the computational bomb; one retained an active 999,999,999-round test and timed out. |
| `MurmurHash3_hash128x64Internal` | 78 / 7 / 100 | 57.6 | Same flow ranged from weak repair to complete correct instruction coverage. |
| `XPathHelper_getSingleStep` | 0 / 0 / 80 | 49.4 | Compile status and effective coverage changed completely in the third repetition. |

These cases establish that one Run3 can be dramatically unlucky. They also show why aggregate correct coverage is more informative than CPR alone.

### Stable-low cases

| Case | New result across three reps | Official five-rep mean | Interpretation |
|---|---|---|---|
| `WalkerNORMALIZE_analyzeMultiText` | compile failed 3/3; correct IC 0 | CPR 100; correct IC 54.8 | Ordinary random resampling did not solve the inaccessible/nested-type construction problem. |
| `StAXStreamBuilder_processPrunableElement` | correct IC 0 in 3/3 | correct IC 6.2 | Compile status moved, but no correct focal coverage appeared. |
| `ByteMachine_addEndOfMatch` | correct IC 0 in 3/3 | correct IC 16.8 | Two nominal compile successes had zero effective tests/coverage; hallucinated production API remained. |

These stable failures are the clearest evidence against “randomness alone.” They point to repair context, generation strategy, source/API grounding, or an official configuration difference.

## Timeout mechanism reproduced

`Sha2Crypt` reproduced the Run3 failure mechanism. The generated test can use `rounds=999999999`. The open-source timeout repair invokes a second verbose run and searches for an old ASCII tree marker (`| | +--`) to identify the hanging test. Java 17's console output uses Unicode tree markers, so the offending method is not reliably removed and can be executed repeatedly during repair.

- rep 1: the final selected test no longer contained the dangerous active input; correct IC/BC = 93/85.
- rep 2: the dangerous test was commented out; correct IC/BC = 93/79.
- rep 3: the dangerous input remained active; EPR and correct coverage were 0.

This is both stochasticity and repair-process weakness: randomness decides whether the dangerous input is generated and whether a later LLM response removes it; the deterministic repair rule fails to provide a robust guardrail.

## Official prompt/context comparison

The new repetitions exactly reproduce the current Run3's fixed prompt inputs: all 60 fixed init/context/case-prompt files match Run3. They do not exactly reproduce official rep 1.

After normalizing whitespace and JSON formatting:

- condition/io/exception case prompts: 36/36 semantically equal to official rep 1;
- init context: 7/12 equal;
- init framework prompt: 0/12 equal;
- usage context: 2/12 equal;
- gencode prompt: 2/12 equal.

Some differences are source formatting, but others change invocation-example ordering/content and the sampled framework/usage context. Thus the official artifacts are not simply five more draws of the exact current end-to-end prompt chain. This is a credible residual explanation, separate from the already-known final/temp provenance issue.

## Factor verdict

| Factor | Evidence strength | Contribution verdict |
|---|---|---|
| A. LLM stochasticity | High | Medium-to-high. It explains large case flips and why Run3's selected failures were unusually bad, but not the remaining official EPR/CPR gap. |
| B. Repair/generation strategy | Very high | High and the strongest actionable factor. The prior paired enhanced-repair test produced simultaneous CPR/EPR/correct-coverage gains, and this experiment reproduced deterministic timeout/API/oracle weaknesses. |
| C. Environment difference | Medium | Low overall. Java/resources were controlled; resources affect full coverage but did not fix wrong assertions. The Unicode timeout-parser interaction is real but narrow. |
| D. Artifact difference | High evidence that it exists | Very low contribution to Run3's score. It limits historical interpretation but does not cause these isolated generation/repair failures. |

Residual evidence is medium-to-high for official prompt/context and possibly provider/backend or hidden experiment settings. All OpenRouter calls returned the requested model string, which argues against an accidental model-name mismatch. Multiple system fingerprints and the stable-low cases mean a backend/configuration contribution cannot yet be excluded. There is still no evidence of a hidden generation algorithm.

## Recommended final reproduction setting

1. Use Java 17 and ensure production resources are copied into the runtime classpath.
2. Use the previously validated enhanced repair prompt plus focal source context; preserve current prompt artifacts and report both raw and KTester-filtered EPR.
3. Add a deterministic guard against computational-bomb parameters and update timeout-test parsing for Unicode JUnit output before any 111-case run.
4. Run at least three repetitions and report mean, range, and per-case flips. Do not present one Run3 as a stable estimate.
5. Before scaling, replay three stable-low cases (`WalkerNORMALIZE`, `StAXStreamBuilder`, `ByteMachine`) with a frozen official prompt and, if available, direct OpenAI versus OpenRouter. This isolates provider/official-setting effects with far less cost than 111 cases.

## Deliverables

- `results/metrics_by_case_and_rep.csv`: Run3, three new reps, and five official reps at case level.
- `results/aggregate_metrics.csv`: group-meeting summary table.
- `results/per_case_variability.csv`: ranges, standard deviations, compile/all-pass flips, and official means.
- `results/prompt_pairing.csv`: prompt hashes across the three new repetitions.
- `results/prompt_source_comparison.csv`: current experiment versus Run3 and official rep 1.
- `results/experiment_summary.json`: aggregate variation and OpenRouter metadata summary.
- `results/factor_evidence.csv`: A/B/C/D evidence assessment.
- `code_diff.patch`: all isolation, instrumentation, and timeout-control differences from the original checkout.
- `rep_1`, `rep_2`, `rep_3`: generation, repair, coverage logs and all artifacts.
- `partial_rep_1_timeout_parser_evidence`: preserved first safety-cap trial showing repeated timeout behavior; excluded from all metrics.
