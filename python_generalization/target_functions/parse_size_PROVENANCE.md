# `parse_size` snapshot provenance

- Project: `python-humanfriendly` (`xolox/python-humanfriendly`)
- Stable version/tag: `10.0`
- Git commit: `6758ac61f906cd8528682003070a57febe4ad3cf`
- Repository: `https://github.com/xolox/python-humanfriendly`
- Upstream focal source: `humanfriendly/__init__.py`, `parse_size(size, binary=False)`
- Upstream focal lines: 198-259
- Snapshot: `target_functions/parse_size_target.py`
- License: MIT; the upstream `LICENSE.txt` is archived with the source evidence.

The stable `10.0` tag and the repository's `master` branch both resolved to the commit
above when this snapshot was prepared on 2026-08-27. Exact upstream files are archived
under `target_functions/provenance/parse_size/upstream/` so AST verification does not
depend on a future network request.

## Integrity hashes

| Artifact | SHA-256 |
|---|---|
| Upstream `humanfriendly/__init__.py` | `b0f08c42fd7a9b7a7cc58c1ddcdde452cd6b7b05490776460c1905d3ff2feafa` |
| Upstream `humanfriendly/text.py` | `fd6046e126786d3e521fde332d475f981e8d5dbbdce200581021264185c9d6c1` |
| Upstream `humanfriendly/compat.py` | `eeaa0518c3458b31a1b39048ca230a4c352adbd0f1cee5c65f8311a192e8e26b` |
| Upstream `humanfriendly/tests.py` | `ddb91ab2b460c347007591478264e8e03507817127947b51a2afedd8c11a7db7` |
| Upstream `LICENSE.txt` | `4ac48f4117809f2734066150450f120b3bb110ac1d3b32170795e0560dbbc1f5` |
| Snapshot module | `f44684d0dcaabeb395c892fac2abfa2c39eb8d8b9ed65d0c982752db7855034c` |
| Canonical focal AST dump | `593796b528b9a2932fc34a7f96d36de034a69087d83e9f40f9697c48fa66868d` |

The AST hash is computed from `ast.dump(function_node, include_attributes=False)`.
Both the upstream and snapshot focal functions produce this same value.

## Dependency mapping

The focal function is copied verbatim. Its AST is checked against the archived upstream
`humanfriendly/__init__.py` by `tests/test_parse_size_target.py`.

Only deterministic local dependencies are embedded in the target module:

- `SizeUnit`, `CombinedUnit`, and `disk_size_units` are copied from upstream
  `humanfriendly/__init__.py`.
- `tokenize()` is copied from upstream `humanfriendly/text.py` with its docstring omitted;
  its executable AST is otherwise unchanged.
- `format()` is copied from upstream `humanfriendly/text.py` with its docstring omitted.
- `is_string()` is specialized to Python 3's `str`; upstream implements the same check
  through its Python 2/3 `basestring` compatibility alias.
- `InvalidSize` keeps the upstream exception type and has no behavior beyond `Exception`;
  its documentation-only body is omitted.
- `collections`, `numbers`, and `re` are Python standard-library modules.

No network, file-system, corpus, database, or third-party runtime dependency is present.
Coverage evaluation reads coverage.py's function-level summary for `parse_size`, so the
embedded helpers and module-level constants do not contribute statements or branches to
the reported focal coverage.
