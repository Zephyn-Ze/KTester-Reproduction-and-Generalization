from target_functions.parse_size_target import parse_size
import pytest

def test_parse_size_normal_cases():
    assert parse_size('42') == 42
    assert parse_size('13b') == 13
    assert parse_size('5 bytes') == 5
    assert parse_size('1 KB') == 1000
    assert parse_size('1 kilobyte') == 1000
    assert parse_size('1 GiB') == 1073741824
    assert parse_size('1.5 GB') == 1500000000
    assert parse_size('1.5 GB', binary=True) == 1610612736

def test_parse_size_binary_cases():
    assert parse_size('1 KB', binary=True) == 1024
    assert parse_size('1 MiB') == 1048576
    assert parse_size('1 GiB', binary=True) == 1073741824

def test_parse_size_edge_cases():
    assert parse_size('0') == 0
    assert parse_size('0 bytes') == 0
    assert parse_size('0 KB') == 0
    assert parse_size('1.0 KB') == 1000
    assert parse_size('2.5 MB') == 2500000

def test_parse_size_invalid_cases():
    with pytest.raises(Exception) as excinfo:
        parse_size('invalid size')
    assert "Failed to parse size!" in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        parse_size('1.5 invalid')
    assert "Failed to parse size!" in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        parse_size('1.5 GB invalid')
    assert "Failed to parse size!" in str(excinfo.value)