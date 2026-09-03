from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_single_quote_normalization():
    assert normalize_string_quotes("'Hello, World!'") == '"Hello, World!"'

def test_already_normalized():
    assert normalize_string_quotes('"Hello, World!"') == '"Hello, World!"'

def test_raw_string_with_unescaped_quotes():
    assert normalize_string_quotes(r"'Hello, 'World'") == r"'Hello, 'World'"

def test_raw_string_with_escaped_quotes():
    assert normalize_string_quotes(r"'Hello, \'World'") == r"'Hello, \'World'"

def test_formatted_string_with_interpolation():
    name = "name"
    assert normalize_string_quotes(r"f'Hello, {name}'") == r"f'Hello, {name}'"

def test_edge_case_ending_with_quote():
    assert normalize_string_quotes('"Hello, World!"') == '"Hello, World!"'

def test_no_quotes_present():
    assert normalize_string_quotes("Hello, World!") == "Hello, World!"

def test_string_with_escaped_quotes():
    assert normalize_string_quotes("'Hello, \\'World'") == '"Hello, \\"World"'

def test_multiple_quotes():
    assert normalize_string_quotes("'Hello, 'World' and 'Universe'") == '"Hello, "World" and "Universe""'

def test_escaped_quotes_in_raw_string():
    assert normalize_string_quotes(r"'Hello, \\'World'") == r"'Hello, \\'World'"

def test_mixed_quotes_with_escaping():
    assert normalize_string_quotes("'Hello, \\"World\\"'") == '"Hello, \\"World\\"'

def test_multiple_escapes():
    assert normalize_string_quotes("'Hello, \\\\World'") == '"Hello, \\\\World"'