from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_single_quote_normalization():
    result = normalize_string_quotes("'Hello, World!'")
    assert result == '"Hello, World!"'

def test_already_normalized_double_quotes():
    result = normalize_string_quotes('"Hello, World!"')
    assert result == '"Hello, World!"'

def test_raw_string_with_unescaped_quotes():
    result = normalize_string_quotes(r'Hello, "World"')
    assert result == r'Hello, "World"'

def test_raw_string_with_escaped_quotes():
    result = normalize_string_quotes(r'Hello, \"World\"')
    assert result == r'Hello, \"World\"'

def test_mixed_quotes_normalization():
    result = normalize_string_quotes("'This is a \"test\" string.'")
    assert result == '"This is a \"test\" string."'

def test_escaped_new_quote_at_end():
    result = normalize_string_quotes('"This is a test string."\\')
    assert result == '"This is a test string.\\"'

def test_multiple_escapes_handling():
    result = normalize_string_quotes("'This is a test string with \\\"escaped quotes\\\".'")
    assert result == '"This is a test string with \\"escaped quotes\\"."'

def test_empty_string_input():
    result = normalize_string_quotes("")
    assert result == ""

def test_prefix_only_with_quotes():
    result = normalize_string_quotes("f'Hello, World!'")
    assert result == "f'Hello, World!'"

def test_malformed_input_without_quotes():
    with pytest.raises(AssertionError):
        normalize_string_quotes("No quotes here")