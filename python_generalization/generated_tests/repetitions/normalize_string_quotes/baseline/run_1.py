from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_normal_cases():
    assert normalize_string_quotes("'Hello, World!'") == '"Hello, World!"'
    assert normalize_string_quotes('"Hello, World!"') == "'Hello, World!'"
    assert normalize_string_quotes("'This is a test.'") == '"This is a test."'
    assert normalize_string_quotes('"This is a test."') == "'This is a test.'"
    assert normalize_string_quotes("'It\'s a nice day.'") == '"It\'s a nice day."'
    assert normalize_string_quotes('"It\'s a nice day."') == "'It\'s a nice day.'"
    assert normalize_string_quotes("'Raw string: r'Test'") == "'Raw string: r'Test'"
    assert normalize_string_quotes('"Raw string: r\"Test\"') == '"Raw string: r\"Test\"'

def test_edge_cases():
    assert normalize_string_quotes("'''Triple quotes'''") == '"""Triple quotes"""'
    assert normalize_string_quotes('"""Triple quotes"""') == "'''Triple quotes'''"
    assert normalize_string_quotes("'Escaped quote: \\\'") == '"Escaped quote: \\\\''
    assert normalize_string_quotes('"Escaped quote: \\"') == "'Escaped quote: \\'"
    assert normalize_string_quotes("'String with {interpolation}'") == '"String with {interpolation}"'
    assert normalize_string_quotes('"String with {interpolation}"') == "'String with {interpolation}'"
    assert normalize_string_quotes("f'Test with {variable}'") == 'f"Test with {variable}"'
    assert normalize_string_quotes('f"Test with {variable}"') == "f'Test with {variable}'"

def test_no_change_cases():
    assert normalize_string_quotes("r'Raw string: r'Test'") == "r'Raw string: r'Test'"
    assert normalize_string_quotes("f'Interpolated: {value}'") == "f'Interpolated: {value}'"
    assert normalize_string_quotes('f"Interpolated: {value}"') == 'f"Interpolated: {value}"'
    assert normalize_string_quotes("f'Test with \\'") == "f'Test with \\'"