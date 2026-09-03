from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_no_quotes():
    s = "This is a plain string."
    assert normalize_string_quotes(s) == s

def test_already_normalized_double_quotes():
    s = '"This is a double quoted string."'
    assert normalize_string_quotes(s) == s

def test_already_normalized_single_quotes():
    s = "'This is a single quoted string.'"
    assert normalize_string_quotes(s) == s

def test_convert_single_to_double_quotes():
    s = "'This is a test string.'"
    expected = '"This is a test string."'
    assert normalize_string_quotes(s) == expected

def test_convert_double_to_single_quotes():
    s = '"This is a test string."'
    expected = "'This is a test string.'"
    assert normalize_string_quotes(s) == expected

def test_raw_string_with_escaped_quotes():
    s = r"'This is a raw string with an escaped quote: \'."
    assert normalize_string_quotes(s) == s

def test_mixed_quotes_and_escapes():
    s = '"This is a test with an escaped quote: \\" and more text.'
    expected = '"This is a test with an escaped quote: \\" and more text."'
    assert normalize_string_quotes(s) == expected

def test_edge_case_ending_with_unescaped_quote():
    s = '"This is a test string without closing quote'
    expected = '"This is a test string without closing quote"'
    assert normalize_string_quotes(s) == expected

def test_nested_escapes():
    s = r"'This is a test with nested escapes: \\\'"
    assert normalize_string_quotes(s) == s

def test_malformed_string():
    s = "This is a malformed string with no quotes."
    with pytest.raises(AssertionError):
        normalize_string_quotes(s)

def test_empty_string():
    s = ""
    assert normalize_string_quotes(s) == s

def test_multiple_quotes():
    s = "'This is a string with 'single' and \"double\" quotes.'"
    expected = '"This is a string with \'single\' and "double" quotes."'
    assert normalize_string_quotes(s) == expected