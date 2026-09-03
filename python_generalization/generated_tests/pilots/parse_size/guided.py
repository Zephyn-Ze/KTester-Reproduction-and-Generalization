from target_functions.parse_size_target import parse_size
import pytest

def test_standard_size_parsing():
    assert parse_size('42') == 42

def test_size_with_unit_in_bytes():
    assert parse_size('13b') == 13

def test_size_with_singular_unit():
    assert parse_size('1 kilobyte') == 1000

def test_size_with_plural_unit():
    assert parse_size('2 megabytes') == 2000000

def test_zero_size():
    assert parse_size('0') == 0

def test_large_value_size():
    assert parse_size('1 YB') == 1000000000000000000

def test_ambiguous_unit_without_binary_flag():
    assert parse_size('1 KB') == 1000

def test_ambiguous_unit_with_binary_flag():
    assert parse_size('1 KB', binary=True) == 1024

def test_multiple_units():
    assert parse_size('1.5 GB') == 1500000000

def test_multiple_units_with_binary_flag():
    assert parse_size('1.5 GB', binary=True) == 1610612736

def test_duplicate_units():
    assert parse_size('1.5 GB 1.5 GB') == 1500000000

def test_invalid_format():
    with pytest.raises(Exception) as excinfo:
        parse_size('abc')
    assert "Failed to parse size!" in str(excinfo.value)

def test_unsupported_units():
    with pytest.raises(Exception) as excinfo:
        parse_size('1 XYZ')
    assert "Failed to parse size!" in str(excinfo.value)

def test_negative_values():
    with pytest.raises(Exception) as excinfo:
        parse_size('-1 KB')
    assert "Failed to parse size!" in str(excinfo.value)

def test_empty_input():
    with pytest.raises(Exception) as excinfo:
        parse_size('')
    assert "Failed to parse size!" in str(excinfo.value)

def test_invalid_decimal_format():
    with pytest.raises(Exception) as excinfo:
        parse_size('1.5.5 GB')
    assert "Failed to parse size!" in str(excinfo.value)