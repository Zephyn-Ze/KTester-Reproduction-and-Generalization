from target_functions.parse_size_target import parse_size
import pytest

def test_parse_integer_size_without_unit():
    assert parse_size('42') == 42

def test_parse_size_with_bytes_unit():
    assert parse_size('13b') == 13

def test_parse_size_with_kilobyte_unit():
    assert parse_size('1 KB') == 1000

def test_parse_size_with_binary_kilobyte_unit():
    assert parse_size('1 KB', binary=True) == 1024

def test_parse_size_with_megabyte_unit():
    assert parse_size('1.5 MB') == 1500000000

def test_parse_size_with_binary_megabyte_unit():
    assert parse_size('1.5 MB', binary=True) == 1572864000

def test_parse_size_with_plural_unit():
    assert parse_size('2 kilobytes') == 2000

def test_parse_size_with_mixed_case_unit():
    assert parse_size('3 GiB') == 3221225472

def test_invalid_size_format_with_unsupported_characters():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('abc')

def test_invalid_size_format_with_multiple_dots():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('1.5.5 GB')

def test_parse_zero_size():
    assert parse_size('0') == 0

def test_parse_size_with_leading_trailing_spaces():
    assert parse_size(' 1 TB ') == 1000000000000

def test_parse_large_size_value():
    assert parse_size('1 YB') == 1000000000000000000

def test_invalid_size_with_none_input():
    with pytest.raises(parse_size.InvalidSize):
        parse_size(None)

def test_invalid_size_with_empty_string():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('')