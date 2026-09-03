from target_functions.parse_size_target import parse_size
import pytest

def test_parse_size_normal_cases():
    assert parse_size('42') == 42
    assert parse_size('13b') == 13
    assert parse_size('5 bytes') == 5
    assert parse_size('1 KB') == 1000
    assert parse_size('1 kilobyte') == 1000
    assert parse_size('1.5 GB') == 1500000000
    assert parse_size('1.5 GB', binary=False) == 1500000000
    assert parse_size('1 KiB') == 1024
    assert parse_size('1.5 GB', binary=True) == 1610612736

def test_parse_size_edge_cases():
    assert parse_size('0') == 0
    assert parse_size('0 bytes') == 0
    assert parse_size('1 B') == 1
    assert parse_size('1.0 B') == 1
    assert parse_size('1 MB') == 1000000
    assert parse_size('1 MiB') == 1048576

def test_parse_size_invalid_cases():
    with pytest.raises(InvalidSize):
        parse_size('invalid size')
    with pytest.raises(InvalidSize):
        parse_size('1.5 invalidunit')
    with pytest.raises(InvalidSize):
        parse_size('')
    with pytest.raises(InvalidSize):
        parse_size('1.5')
    with pytest.raises(InvalidSize):
        parse_size('1.5 GB invalid')