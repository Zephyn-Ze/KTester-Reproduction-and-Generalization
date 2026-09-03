from target_functions.normalize_string_quotes_target import normalize_string_quotes
import pytest

def test_normal_cases():
    assert normalize_string_quotes("'Hello'") == '"Hello"'
    assert normalize_string_quotes('"Hello"') == "'Hello'"
    assert normalize_string_quotes("'Hello, \"world\"'") == '"Hello, \\"world\\""'
    assert normalize_string_quotes('"Hello, \\"world\\""') == "'Hello, \\"world\\""'
    assert normalize_string_quotes("'Hello, \\\\world\\\\'") == '"Hello, \\\\world\\\\"'
    assert normalize_string_quotes('f"Hello, {name}"') == 'f"Hello, {name}"'
    assert normalize_string_quotes('r"Hello, \\"world\\""') == 'r"Hello, \\"world\\""'

def test_edge_cases():
    assert normalize_string_quotes('"""Hello"""') == '"""Hello"""'
    assert normalize_string_quotes("'''Hello'''") == '"""Hello"""'
    assert normalize_string_quotes('r"""Hello"""') == 'r"""Hello"""'
    assert normalize_string_quotes('f"""Hello"""') == 'f"""Hello"""'
    assert normalize_string_quotes('f"Hello, {name}"') == 'f"Hello, {name}"'
    assert normalize_string_quotes('f"Hello, \\\\{name}"') == 'f"Hello, \\\\{name}"'
    assert normalize_string_quotes('"""Hello, \\"world\\""') == '"""Hello, \\"world\\""'
    assert normalize_string_quotes("'''Hello, \\"world\\""") == '"""Hello, \\"world\\""'
    assert normalize_string_quotes("'") == '"'
    assert normalize_string_quotes('') == ''