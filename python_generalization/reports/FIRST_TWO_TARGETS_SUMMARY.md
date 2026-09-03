# First two Python targets: preserved summary

The first two pilot targets predate the generalized evaluator and per-target artifact layout used for Targets 3-5. Their generated test files are retained, but the later machine-readable `evaluation.json` format is not available for these two targets in the preserved directory. The values below are therefore reported from the subsequently written Target 3 and Target 5 cross-target summaries.

## `parse_bindings`

- Baseline EPR: 80.00% (20/25).
- Guided EPR: 86.11% (31/36) among four collecting runs.
- One additional Guided file failed collection.
- Mean correct coverage across all five runs was 80% for both strategies when the non-collecting run was counted as zero.
- Coverage saturated on the small focal function (13 statements, 8 branches).

## `is_main_conference`

- Baseline EPR: 65.00% (13/20).
- Guided EPR: 60.00% (30/50).
- Both strategies averaged 94.12% raw statement and 90.00% raw branch coverage.
- Correct statement coverage tied at 90.59%; Guided correct branch coverage was 86.00% versus Baseline 84.00%.
- The main semantic failure was misunderstanding the local `ASE -> kbse` and `FSE -> sigsoft` mapping.

These two targets are retained as early exploratory evidence, not presented as having the same artifact completeness as Targets 3-5.

