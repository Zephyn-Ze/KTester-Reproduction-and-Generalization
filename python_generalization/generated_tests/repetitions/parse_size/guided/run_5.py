from target_functions.parse_size_target import parse_size
import pytest

def test_parse_simple_size():
    assert parse_size('42') == 42

def test_parse_size_in_bytes():
    assert parse_size('13b') == 13

def test_parse_size_with_unit():
    assert parse_size('1 KB') == 1000

def test_parse_ambiguous_size_decimal():
    assert parse_size('1 K') == 1000

def test_parse_ambiguous_size_binary():
    assert parse_size('1 K', binary=True) == 1024

def test_parse_plural_unit():
    assert parse_size('1 kilobyte') == 1000

def test_parse_decimal_size():
    assert parse_size('1.5 GB') == 1500000000

def test_parse_decimal_size_binary():
    assert parse_size('1.5 GB', binary=True) == 1610612736

def test_parse_zero_value():
    assert parse_size('0 KB') == 0

def test_parse_empty_input():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('')

def test_parse_invalid_format():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('abc')

def test_parse_unsupported_unit():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('1 XYZ')

def test_parse_non_string_input():
    with pytest.raises(parse_size.InvalidSize):
        parse_size(42)

def test_parse_large_size():
    assert parse_size('1 YB') == 1000000000000000000

def test_parse_complex_size():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('2.5 TB and 500 MB')