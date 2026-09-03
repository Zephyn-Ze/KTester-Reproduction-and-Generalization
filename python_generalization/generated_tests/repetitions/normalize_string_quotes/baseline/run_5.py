from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_normal_cases():
    assert normalize_string_quotes("'Hello World'") == '"Hello World"'
    assert normalize_string_quotes('"Hello World"') == "'Hello World'"
    assert normalize_string_quotes("'''Hello World'''") == '"""Hello World"""'
    assert normalize_string_quotes('"""Hello World"""') == '"""Hello World"""'
    assert normalize_string_quotes("'Hello \\\"World'") == '"Hello \\"World"'
    assert normalize_string_quotes('"Hello \\"World"') == "'Hello \\"World"'


def test_raw_strings():
    assert normalize_string_quotes(r"'Hello \\"World'") == r"'Hello \\"World'"
    assert normalize_string_quotes(r'"Hello \\"World"') == r'"Hello \\"World"'
    assert normalize_string_quotes(r"'''Hello \\"World'''") == r"'''Hello \\"World'''"
    assert normalize_string_quotes(r'"""Hello \\"World"""') == r'"""Hello \\"World"""'


def test_f_strings():
    assert normalize_string_quotes(f"'Hello {name}'") == f'"Hello {name}"'
    assert normalize_string_quotes(f'"Hello {name}"') == f"'{name}'"
    assert normalize_string_quotes(f"'''Hello {name}'''") == f'"""Hello {name}"""'
    assert normalize_string_quotes(f'"""Hello {name}"""') == f'"""Hello {name}"""'


def test_edge_cases():
    assert normalize_string_quotes('"""Hello World"') == '"""Hello World"'
    assert normalize_string_quotes('"Hello World"') == "'Hello World'"
    assert normalize_string_quotes("'") == '"'
    assert normalize_string_quotes('"""') == '"""'
    assert normalize_string_quotes('""') == '""'
    assert normalize_string_quotes("''") == '""'
    assert normalize_string_quotes('"""Hello \\\\ World"""') == '"""Hello \\\\ World"""'
    assert normalize_string_quotes(r"'Hello {\\'World'}'") == r'"Hello {\\'World'}"'
    assert normalize_string_quotes(r'"Hello {\\'World'}"') == r"'Hello {\\'World'}'"