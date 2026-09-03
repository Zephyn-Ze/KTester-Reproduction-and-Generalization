# A/B experiment record: `JsonReader.nextUnquotedValue`

Prepared: 2026-08-20  
Project: Gson / KTester

## Scope and safeguards

- KTester core code and every `pom.xml` were left unchanged.
- No existing evaluation, diagnostic, backup, or isolation directory was removed, renamed, or restored.
- This record copies existing generation artifacts only; it does **not** claim a fresh, controlled re-generation.

## Conditions

| Metric | A: original prompt | B: modified prompt |
|---|---:|---:|
| Private-method instruction | “Use reflection if the focal method is private.” | Prohibits reflection and requires indirect testing through public callers. |
| Archived generated test selected | `JsonReader_nextUnquotedValue_Test_2.java` | Current `JsonReader_nextUnquotedValue_Test.java` |
| `@Test` annotations | 19 | 2 |
| `getDeclaredMethod` / `setAccessible` occurrences | 2 / 2 | 0 / 0 |
| Reflection used | yes | no |
| Compile status | not independently re-run for this archived artifact | not independently re-run for this current artifact |
| Execution status | archived repair feedback: 3 passed, 16 failed | no clean same-artifact execution log located |
| Focal-method line / branch coverage | not available | not available |
| Correct coverage | not available | not available |

## Evidence and interpretation

The source prompt differs exactly on the private-method instruction. The original-prompt test directly invokes `nextUnquotedValue()` through `getDeclaredMethod()` and `setAccessible(true)`. The modified-prompt test calls `JsonReader.nextName()` and `nextString()` instead, so it has no direct private-method access.

The available JaCoCo CSV is a project-wide class report, not a clean per-focal-method measurement for independently executed A and B artifacts. Therefore its line and branch totals must not be used for this comparison. Likewise, the archived execution feedback belongs to a repair iteration and cannot prove the execution outcome of the copied original test without a rerun.

## Next controlled run

1. Create a separate disposable evaluation work area for each condition, leaving the current isolation intact.
2. Regenerate each condition once from its saved prompt and retain the model response and command log.
3. Run compile and test execution against the corresponding generated file only.
4. Produce a separate JaCoCo report for each run; extract the `JsonReader` row and focal-method coverage only if the report supports that level of granularity.
5. Update this table with those run-specific outcomes; do not overwrite the copied artifacts.
