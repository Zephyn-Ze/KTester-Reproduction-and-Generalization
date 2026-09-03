from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_convert_single_quotes_to_double_quotes():
    s = "'Hello, World!'"
    expected = '"Hello, World!"'
    assert normalize_string_quotes(s) == expected

def test_convert_double_quotes_to_single_quotes():
    s = '"Hello, World!"'
    expected = "'Hello, World!'"
    assert normalize_string_quotes(s) == expected

def test_raw_string_with_unescaped_quotes():
    s = r"'Hello, 'World!'"
    expected = r"'Hello, 'World!'"
    assert normalize_string_quotes(s) == expected

def test_raw_string_with_escaped_quotes():
    s = r"'Hello, \'World!'"
    expected = r"'Hello, \'World!'"
    assert normalize_string_quotes(s) == expected

def test_double_quotes_with_escaped_quotes():
    s = '"Hello, \\"World!\\""' 
    expected = '"Hello, \\"World!\\""' 
    assert normalize_string_quotes(s) == expected

def test_triple_quotes_handling():
    s = '"""Hello, World!"""'
    expected = '"""Hello, World!"""'
    assert normalize_string_quotes(s) == expected

def test_string_ending_with_a_quote():
    s = '"Hello, World!'
    expected = '"Hello, World!'
    assert normalize_string_quotes(s) == expected

def test_multiple_escaped_quotes():
    s = '"He said, \\"Hello, World!\\""' 
    expected = '"He said, \\"Hello, World!\\""' 
    assert normalize_string_quotes(s) == expected

def test_interpolated_string():
    name = "Alice"
    s = f"'Hello, {name}!'"
    expected = f"'Hello, {name}!'"
    assert normalize_string_quotes(s) == expected

def test_string_with_no_quotes():
    s = 'Hello, World!'
    expected = 'Hello, World!'
    assert normalize_string_quotes(s) == expected

def test_malformed_string_with_no_quotes():
    s = 'Hello World'
    with pytest.raises(AssertionError):
        normalize_string_quotes(s)