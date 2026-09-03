from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_normal_cases():
    assert normalize_string_quotes('"Hello, World!"') == "'Hello, World!'"
    assert normalize_string_quotes("'Hello, World!'") == '"Hello, World!"'
    assert normalize_string_quotes('"This is a test."') == "'This is a test.'"
    assert normalize_string_quotes("'This is a test.'") == '"This is a test."'
    assert normalize_string_quotes('"Escaped quote: \\" here."') == "'Escaped quote: \\' here.'"
    assert normalize_string_quotes("'Escaped quote: \\' here.'") == '"Escaped quote: \\" here."'
    assert normalize_string_quotes('"Raw string: r\\"Hello, World!\\"."') == '"Raw string: r\\"Hello, World!\\"."'
    assert normalize_string_quotes("'Raw string: r\\'Hello, World!\\'." ) == "'Raw string: r\\'Hello, World!\\'."

def test_edge_cases():
    assert normalize_string_quotes('"""Triple quoted string"""') == '"""Triple quoted string"""'
    assert normalize_string_quotes("'''Triple quoted string'''") == '"""Triple quoted string"""'
    assert normalize_string_quotes('"Unescaped quote: " here."') == "'Unescaped quote: ' here.'"
    assert normalize_string_quotes("'Unescaped quote: ' here.'") == '"Unescaped quote: " here."'
    assert normalize_string_quotes('"Mixed quotes: \' here."') == "'Mixed quotes: \\\" here.'"
    assert normalize_string_quotes("'Mixed quotes: \" here.'") == '"Mixed quotes: \\" here."'
    assert normalize_string_quotes("r'Raw string with \\'") == "r'Raw string with \\'"
    assert normalize_string_quotes("f'Formatted string: {value}'") == "f'Formatted string: {value}'"
    assert normalize_string_quotes('f"Formatted string with a quote: \\"') == 'f"Formatted string with a quote: \\"'

def test_no_change_cases():
    assert normalize_string_quotes('"Hello, \\"World!\\""') == '"Hello, \\"World!\\""'
    assert normalize_string_quotes("'Hello, \\'World!\\'") == "'Hello, \\'World!\\'"
    assert normalize_string_quotes('r"Raw string: \\"') == 'r"Raw string: \\"'
    assert normalize_string_quotes('f"Formatted string: {value}"') == 'f"Formatted string: {value}"'