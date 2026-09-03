from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_convert_single_quote_to_double_quote():
    assert normalize_string_quotes("'Hello, World!'") == '"Hello, World!"'

def test_double_quote_with_escaped_characters():
    assert normalize_string_quotes('"Hello, \\"World!\\" "') == '"Hello, \\"World!\\" "'

def test_raw_string_with_unescaped_quotes():
    assert normalize_string_quotes("r'Hello, \"World!\"'") == "r'Hello, \"World!\"'"

def test_edge_case_with_ending_quote():
    assert normalize_string_quotes('"Hello, World!"') == '"Hello, World!"'

def test_multiple_prefix_characters():
    assert normalize_string_quotes("ft'Hello, World!'") == 'f"Hello, World!"'

def test_no_quotes_present():
    assert normalize_string_quotes("Hello, World!") == "Hello, World!"

def test_already_normalized_string():
    assert normalize_string_quotes('"Hello, World!"') == '"Hello, World!"'

def test_escaped_quotes_in_raw_string():
    assert normalize_string_quotes("r'Hello, \\'World!\\''") == "r'Hello, \\'World!\\''"

def test_formatted_string_with_interpolation():
    name = "User"
    assert normalize_string_quotes(f"f'Hello, {name}!'") == f"f'Hello, {name}!'"

def test_malformed_string():
    with pytest.raises(AssertionError):
        normalize_string_quotes("Hello, World!")