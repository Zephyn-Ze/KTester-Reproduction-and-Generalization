from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_normal_cases():
    assert normalize_string_quotes("'Hello World'") == '"Hello World"'
    assert normalize_string_quotes('"Hello World"') == "'Hello World'"
    assert normalize_string_quotes("'Hello \"World\"'") == '"Hello \\"World\\""'
    assert normalize_string_quotes('"Hello \\"World\\""') == "'Hello \\"World\\"'"
    assert normalize_string_quotes("'Hello \\\\World'") == '"Hello \\\\World"'
    assert normalize_string_quotes('"Hello \\\\World"') == "'Hello \\\\World'"

def test_raw_strings():
    assert normalize_string_quotes(r"'Hello \"World\"'") == r'"Hello \"World\""'
    assert normalize_string_quotes(r'"Hello \"World\""') == r"'Hello \"World\"'"
    assert normalize_string_quotes(r"'Hello \\World'") == r'"Hello \\World"'
    assert normalize_string_quotes(r'"Hello \\World"') == r"'Hello \\World'"

def test_interpolated_strings():
    assert normalize_string_quotes(f"'Hello {{}World}'") == '"Hello {{}World}"'
    assert normalize_string_quotes(f'"Hello {{}World}"') == "'Hello {{}World}'"
    assert normalize_string_quotes(f"'Hello {{\\World}}'") == '"Hello {{\\World}}"'
    assert normalize_string_quotes(f'"Hello {{\\World}} "') == "'Hello {{\\World}} '"

def test_edge_cases():
    assert normalize_string_quotes("'''Hello World'''") == "'''Hello World'''"
    assert normalize_string_quotes('"""Hello World"""') == '"""Hello World"""'
    assert normalize_string_quotes('"""Hello \\"World\\""') == '"""Hello \\"World\\""'
    assert normalize_string_quotes("'") == '"'
    assert normalize_string_quotes('"""') == '"""'
    assert normalize_string_quotes("''") == '""'
    assert normalize_string_quotes("") == '""'