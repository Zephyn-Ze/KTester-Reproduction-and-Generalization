import ast
from pathlib import Path

import pytest

from target_functions.parse_size_target import InvalidSize, parse_size


PROJECT_DIR = Path(__file__).resolve().parents[1]
SNAPSHOT = PROJECT_DIR / "target_functions/parse_size_target.py"
UPSTREAM = (
    PROJECT_DIR
    / "target_functions/provenance/parse_size/upstream/humanfriendly/__init__.py"
)


def function_ast(path, name):
    tree = ast.parse(path.read_text())
    function = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name
    )
    return ast.dump(function, include_attributes=False)


def test_parse_size_ast_matches_upstream_10_0():
    assert function_ast(SNAPSHOT, "parse_size") == function_ast(UPSTREAM, "parse_size")


@pytest.mark.parametrize(
    ("text", "binary", "expected"),
    [
        ("42", False, 42),
        ("13b", False, 13),
        ("5 bytes", False, 5),
        ("1 KB", False, 1000),
        ("1 KB", True, 1024),
        ("1 KiB", False, 1024),
        ("1 KiB", True, 1024),
        ("2 kilobytes", False, 2000),
        ("2 kilobytes", True, 2048),
        ("1.5 GB", False, 1500000000),
        ("1.5 GB", True, 1610612736),
        ("1 kitten", False, 1000),
        ("1 KB extra", False, 1000),
    ],
)
def test_parse_size_contract(text, binary, expected):
    assert parse_size(text, binary=binary) == expected


@pytest.mark.parametrize("text", ["1 q", "not-a-size", "1 q extra", ""])
def test_invalid_size_contract(text):
    with pytest.raises(InvalidSize):
        parse_size(text)
