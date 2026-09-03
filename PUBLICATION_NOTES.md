# Publication notes

## Included

- The compact 111-focal-method local evaluator summary.
- Public, path-sanitized diagnosis and artifact-provenance findings, including the complete evidence-by-evidence long report.
- Compact controlled-repair and stochasticity reports with their supporting CSV/JSON tables.
- Five Python target snapshots, frozen prompts, generated tests, Guided Stage 1/2 artifacts where available, evaluation records, provenance notes, and contract tests.
- MIT license texts and archived evidence for the two third-party Python targets.

## Deliberately excluded

- The complete upstream KTester checkout: no license file was found, and republishing it would duplicate the official repository.
- KTester's prompt templates and implementation patches: excluded under the same license boundary.
- Downloaded Maven projects, dataset projects, project indexes, official evaluation archives, dependency jars, build outputs, and coverage HTML: upstream or generated bulk content not needed for the public evidence package.
- Local `.env` files, shell configuration, IDE state, virtual environments, caches, `.coverage` files, logs, raw API responses, request metadata, and settings files: credential/privacy risk, machine-specific state, or unnecessary bulk.
- Full isolated A/B and repetition worktrees: hundreds of megabytes to gigabytes and mostly duplicated upstream/project/build material. Compact reports and source-of-truth tables are retained instead.
- Presentation decks and backups: communication artifacts outside this repository's experimental evidence scope.

The original directories and experiment outputs remain on the local machine unchanged.

## Sanitization

Public copies of Python evaluation JSON replace local absolute interpreter, workspace, and temporary coverage paths with descriptive placeholders. Metrics, test identifiers, failures, and coverage values are unchanged. Original JSON files remain preserved in the local experiment directory.
