# Target 5 provenance: Black normalize_string_quotes

## Upstream identity

- Project: psf/black
- Stable release: 26.5.1
- Commit: 87928e6d6761a4a6d22250e1fee5601b3998086e
- Repository: https://github.com/psf/black
- Source path: src/black/strings.py
- Source link: https://github.com/psf/black/blob/26.5.1/src/black/strings.py#L169-L239
- License: MIT (archived as upstream/LICENSE.txt)
- PyPI release: https://pypi.org/project/black/26.5.1/

The focal function is `normalize_string_quotes(s: str) -> str`, lines 169-239
in the archived upstream file. It is copied verbatim into
`target_functions/normalize_string_quotes_target.py`.

## Snapshot dependency mapping

The snapshot contains only the focal function and its deterministic local dependencies:

- `STRING_PREFIX_CHARS`: exact upstream constant value `"fturbFTURB"`.
- `sub_twice`: exact upstream helper from lines 29-35.
- `_cached_compile`: exact upstream helper from lines 165-166, including its
  `@lru_cache(maxsize=64)` decorator.
- Standard-library imports only: `re`, `functools.lru_cache`,
  `re.Pattern`, and `typing.Final`.

Black's unrelated width-table and parser-tree imports are deliberately excluded because
the focal function does not reference them. No network, filesystem, environment, database,
corpus, plotting, or third-party runtime dependency remains in the snapshot.

## Integrity

- Archived `strings.py` SHA-256:
  `2a1cde3d2de9f88bdf9ef88bc2a4c4e02afe822afe5bd09fb631bb9b7bdf9fae`
- Archived `LICENSE.txt` SHA-256:
  `9c0428f0c3b4779850cf5bd96e11aaa8afc72d4a86d4a36223d7aba2e58d6e00`
- Snapshot SHA-256:
  `3eb436c70b56c68c5f2fe488def273e8031f15882a521400f7d376f57176eb27`
- Canonical focal AST SHA-256 (attributes excluded):
  `06d48905c38db6cf534e7c8eca0656a96055714613c994d43b9e446ed98059de`

The contract suite independently compares the snapshot focal AST with the archived
upstream focal AST.
