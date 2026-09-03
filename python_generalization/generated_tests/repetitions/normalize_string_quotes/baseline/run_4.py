from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_normal_cases():
    assert normalize_string_quotes("'Hello World'") == '"Hello World"'
    assert normalize_string_quotes('"Hello World"') == "'Hello World'"
    assert normalize_string_quotes("'This is a test'") == '"This is a test"'
    assert normalize_string_quotes('"This is a test"') == "'This is a test'"
    assert normalize_string_quotes("'String with \\\"escaped quotes\\\"'") == '"String with \\"escaped quotes\\""'
    assert normalize_string_quotes('"String with \\"escaped quotes\\""') == "'String with \\"escaped quotes\\""'

def test_raw_strings():
    assert normalize_string_quotes(r"'Raw string with \\"escaped quotes\\"'") == r"'Raw string with \\"escaped quotes\\"'"
    assert normalize_string_quotes(r'"Raw string with \\"escaped quotes\\""') == r'"Raw string with \\"escaped quotes\\""'
    assert normalize_string_quotes(r"'Raw string with unescaped \"quotes\"'") == r"'Raw string with unescaped \"quotes\"'"

def test_interpolated_strings():
    assert normalize_string_quotes(f"'String with {{variable}}'") == f'"String with {{variable}}"'
    assert normalize_string_quotes(f'"String with {{variable}} "') == f"'String with {{variable}} '"

def test_edge_cases():
    assert normalize_string_quotes("'''Triple single quotes'''") == "'''Triple single quotes'''"
    assert normalize_string_quotes('"""Triple double quotes"""') == '"""Triple double quotes"""'
    assert normalize_string_quotes("'String with {unmatched'") == "'String with {unmatched'"
    assert normalize_string_quotes('"String with unmatched}') == '"String with unmatched}'
    assert normalize_string_quotes('"""Escaped quote at the end"""') == '"""Escaped quote at the end"""'
    assert normalize_string_quotes("'Escaped quote at the end\\'") == '"Escaped quote at the end\\"'
    assert normalize_string_quotes('"Escaped quote at the end\\"') == "'Escaped quote at the end\\'"

def test_no_change_cases():
    assert normalize_string_quotes('"No change needed"') == '"No change needed"'
    assert normalize_string_quotes("'No change needed'") == "'No change needed'"
    assert normalize_string_quotes('"Already escaped \\"quote\\""') == '"Already escaped \\"quote\\""'
    assert normalize_string_quotes("'Already escaped \\'quote\\'") == "'Already escaped \\'quote\\'"