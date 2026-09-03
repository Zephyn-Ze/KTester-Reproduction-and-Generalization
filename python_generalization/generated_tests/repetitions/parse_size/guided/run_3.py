from target_functions.parse_size_target import parse_size
import pytest

def test_basic_size_parsing():
    assert parse_size('42') == 42

def test_size_with_unit_decimal():
    assert parse_size('1 KB') == 1000

def test_size_with_unit_binary():
    assert parse_size('1 KB', binary=True) == 1024

def test_size_with_plural_unit_decimal():
    assert parse_size('1 kilobyte') == 1000

def test_size_with_plural_unit_binary():
    assert parse_size('1 kibibyte', binary=True) == 1024

def test_floating_point_size():
    assert parse_size('1.5 GB') == 1500000000

def test_floating_point_size_binary():
    assert parse_size('1.5 GB', binary=True) == 1610612736

def test_invalid_size_string():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('1 XYZ')

def test_empty_input():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('')

def test_invalid_format():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('1.5.2 GB')

def test_large_size_value():
    assert parse_size('1 YB') == 1000000000000000000

def test_mixed_case_units():
    assert parse_size('1 Mb') == 1000000

def test_tokenization_of_numbers_with_units():
    assert parse_size('5 bytes') == 5

def test_tokenization_with_extra_spaces():
    assert parse_size('   3   MB   ') == 3000000