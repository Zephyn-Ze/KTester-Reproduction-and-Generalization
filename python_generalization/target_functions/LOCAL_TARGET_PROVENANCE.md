# Local target provenance

The first three targets were extracted from the user's existing PaperAnalysis utility code and frozen as standalone functions for the experiment. Network, filesystem, configuration, and command-line behavior from the surrounding modules was intentionally excluded.

| Target | Original local module | Original file SHA-256 | Snapshot SHA-256 |
|---|---|---|---|
| `parse_bindings` | `Version 3/src/crawler_pro.py`, lines 94-112 | `a310513d89b2364869b056d887b02953b62bf5e4461166512fa6dda1df660b1b` | `64c972217d8f56bf0b2e62580460d19aa7467c2b821a364a33de30f2a584b636` |
| `is_main_conference` | `Version 3/src/inventory.py`, lines 175-199 | `8035ce328d1dcfa495872960dd6775f78a607231a7dd75f2037e843d0b9253a5` | `7c939529aa1a48c565f15b0f101969643622689a3d30eea63a9b74bd68dce1c8` |
| `generate_manifest_template` | `Version 3/src/inventory.py`, lines 120-151 | `8035ce328d1dcfa495872960dd6775f78a607231a7dd75f2037e843d0b9253a5` | `74e260e3775a7b2bd028e28a88d964ca23e98f2538aee1151447223432e0675f` |

The original local module paths are intentionally described without publishing the user's absolute home-directory path. The frozen snapshots preserve the executable function bodies; `is_main_conference_target.py` adds only the required standard-library `re` import.

