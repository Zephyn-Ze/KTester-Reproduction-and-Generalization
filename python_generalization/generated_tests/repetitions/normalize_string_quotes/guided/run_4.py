from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_triple_double_quotes_unchanged():
    s = '"""This is a test."""'
    assert normalize_string_quotes(s) == '"""This is a test."""'

def test_triple_single_quotes_unchanged():
    s = "'''This is a test.'''" 
    assert normalize_string_quotes(s) == "'''This is a test.'''" 

def test_single_quote_to_double_quote_conversion():
    s = "'This is a test.'"
    assert normalize_string_quotes(s) == '"This is a test."'

def test_double_quote_to_single_quote_conversion():
    s = '"This is a test."'
    assert normalize_string_quotes(s) == "'This is a test.'"

def test_raw_string_with_escaped_quotes():
    s = r'\'This is a test.\''
    assert normalize_string_quotes(s) == r'\'This is a test.\''

def test_normal_string_with_escaped_quotes():
    s = '"This is a test with an escaped quote: \\"'
    assert normalize_string_quotes(s) == '"This is a test with an escaped quote: \\"'

def test_empty_string_input():
    s = ''
    assert normalize_string_quotes(s) == ''

def test_string_without_quotes():
    s = 'This is a test.'
    assert normalize_string_quotes(s) == 'This is a test.'

def test_formatted_string_with_escape_characters():
    s = r'f"This is a test with {value}."'
    assert normalize_string_quotes(s) == r'f"This is a test with {value}."'

def test_malformed_string_input():
    s = 'This string has no quotes'
    with pytest.raises(AssertionError):
        normalize_string_quotes(s)

def test_raw_string_with_unescaped_new_quote():
    s = r'This is a test with an unescaped quote: "'
    assert normalize_string_quotes(s) == r'This is a test with an unescaped quote: "'

def test_edge_case_with_last_character_as_quote():
    s = '"This is a test."'
    assert normalize_string_quotes(s) == '"This is a test.\\"'