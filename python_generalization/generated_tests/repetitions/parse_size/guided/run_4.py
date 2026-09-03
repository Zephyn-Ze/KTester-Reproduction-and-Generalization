from target_functions.parse_size_target import parse_size
import pytest

def test_basic_integer_input():
    assert parse_size('42') == 42

def test_input_with_bytes_unit():
    assert parse_size('13b') == 13

def test_input_with_singular_unit():
    assert parse_size('1 KB') == 1000

def test_input_with_plural_unit():
    assert parse_size('1 kilobyte') == 1000

def test_input_with_binary_unit():
    assert parse_size('1 KiB') == 1024

def test_input_with_decimal_value():
    assert parse_size('1.5 GB') == 1500000000

def test_input_with_ambiguous_unit_binary():
    assert parse_size('1 KB', binary=True) == 1024

def test_input_with_extremely_large_size():
    assert parse_size('1 YB') == 1000000000000000000

def test_input_with_invalid_format():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('abc')

def test_input_with_multiple_decimal_points():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('1.5.5 GB')

def test_input_with_singular_and_plural_units():
    assert parse_size('1 byte') == 1
    assert parse_size('1 bytes') == 1

def test_input_with_ambiguous_unit_decimal():
    assert parse_size('1 K', binary=False) == 1000