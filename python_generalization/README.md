# Lightweight Python generalization

This directory preserves a small Baseline-versus-Guided experiment over five Python functions. It tests a mechanism inspired by KTester; it is not a Python implementation of the full KTester system.

## Design

- Baseline: source code directly to pytest generation.
- Guided Stage 1: extract behavioral/testing knowledge.
- Guided Stage 2: design concrete scenarios.
- Guided Stage 3: generate pytest code from source, knowledge, and scenarios.
- Model: `openai/gpt-4o-mini-2024-07-18`.
- Temperature: `0.5`.
- Formal repetitions: five Baseline and five Guided generations per target where the formal protocol was completed.
- Generated tests were evaluated exactly as returned; syntax errors and collection failures were preserved rather than repaired.

## Measurement

EPR is the number of passing pytest test methods divided by collected generated test methods. A generated file that fails collection has no methods in that denominator, so every result must also report collection success. Raw coverage executes all collecting methods; correct coverage is recalculated using passing methods only. Both are restricted to the focal function rather than the whole snapshot module.

The target reports contain the complete target-specific tables and failure classifications. `FIFTH_TARGET_EXPERIMENT_REPORT.md` also provides a unified five-target summary.

## Reproduction boundary

The API key is not stored. Generation requires an `OPENROUTER_API_KEY` environment variable. Existing generated artifacts can be inspected and contract tests can be run without making API requests.

Use a new output directory for any rerun. Do not overwrite the evidence in `generated_tests/`.

