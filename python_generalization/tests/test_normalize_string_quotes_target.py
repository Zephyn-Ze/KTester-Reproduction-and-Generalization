import ast
from pathlib import Path

import pytest

from target_functions.normalize_string_quotes_target import normalize_string_quotes


PROJECT_DIR = Path(__file__).resolve().parents[1]


def function_ast(path, function_name):
    tree = ast.parse(path.read_text())
    return next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    )


def test_focal_ast_matches_archived_upstream():
    upstream = PROJECT_DIR / (
        "target_functions/provenance/normalize_string_quotes/upstream/black/strings.py"
    )
    snapshot = PROJECT_DIR / "target_functions/normalize_string_quotes_target.py"
    assert ast.dump(
        function_ast(snapshot, "normalize_string_quotes"), include_attributes=False
    ) == ast.dump(
        function_ast(upstream, "normalize_string_quotes"), include_attributes=False
    )


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("'hello'", '"hello"'),
        ('"hello"', '"hello"'),
        ("b'bytes'", 'b"bytes"'),
        ("R'regex'", 'R"regex"'),
        ("'''line'''", '\"\"\"line\"\"\"'),
        ('\"\"\"line\"\"\"', '\"\"\"line\"\"\"'),
        ("'don\\'t'", '"don\'t"'),
        ('"say \\"hi\\""', "'say \"hi\"'"),
        ("'He said \"hi\"'", "'He said \"hi\"'"),
        ('"don\'t"', '"don\'t"'),
        (r"r'path\name'", 'r"path\\name"'),
        ("r'has\"quote'", "r'has\"quote'"),
        (r'''r"has'quote"''', r'''r"has'quote"'''),
        ("f'{value}'", 'f"{value}"'),
        (r"f'{path\name}'", r"f'{path\name}'"),
        ("'''end\"'''", "'''end\"'''"),
    ],
)
def test_quote_normalization_contract(source, expected):
    assert normalize_string_quotes(source) == expected


def test_empty_input_raises_index_error():
    with pytest.raises(IndexError):
        normalize_string_quotes("")


def test_missing_quote_raises_assertion_error():
    with pytest.raises(AssertionError, match="Malformed string"):
        normalize_string_quotes("plain")

