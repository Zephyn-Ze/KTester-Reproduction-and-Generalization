from target_functions.parse_size_target import parse_size
import pytest

def test_basic_integer_input():
    assert parse_size("42") == 42

def test_input_with_bytes_unit():
    assert parse_size("13b") == 13

def test_input_with_full_unit_name():
    assert parse_size("5 bytes") == 5

def test_input_with_kilobyte_unit():
    assert parse_size("1 KB") == 1000

def test_input_with_binary_kilobyte_unit():
    assert parse_size("1 KiB") == 1024

def test_ambiguous_unit_with_decimal():
    assert parse_size("1 KB", binary=False) == 1000

def test_ambiguous_unit_with_binary():
    assert parse_size("1 KB", binary=True) == 1024

def test_fractional_input():
    assert parse_size("1.5 GB") == 1500000000

def test_fractional_input_with_binary():
    assert parse_size("1.5 GB", binary=True) == 1610612736

def test_zero_input():
    assert parse_size("0") == 0

def test_large_size_input():
    assert parse_size("1 YB") == 1000000000000000000

def test_invalid_format():
    with pytest.raises(Exception) as excinfo:
        parse_size("invalid input")
    assert "Failed to parse size!" in str(excinfo.value)

def test_special_characters():
    with pytest.raises(Exception) as excinfo:
        parse_size("5#MB")
    assert "Failed to parse size!" in str(excinfo.value)

def test_empty_input():
    with pytest.raises(Exception) as excinfo:
        parse_size(" ")
    assert "Failed to parse size!" in str(excinfo.value)

def test_duplicate_unit_specification():
    with pytest.raises(Exception) as excinfo:
        parse_size("1 KB KB")
    assert "Failed to parse size!" in str(excinfo.value)