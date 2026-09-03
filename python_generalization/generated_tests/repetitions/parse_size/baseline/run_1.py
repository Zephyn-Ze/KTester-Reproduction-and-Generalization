from target_functions.parse_size_target import parse_size
import pytest

def test_parse_size_normal_cases():
    assert parse_size('42') == 42
    assert parse_size('13b') == 13
    assert parse_size('5 bytes') == 5
    assert parse_size('1 KB') == 1000
    assert parse_size('1 kilobyte') == 1000
    assert parse_size('1 KiB') == 1024
    assert parse_size('1.5 GB') == 1500000000
    assert parse_size('1.5 GB', binary=True) == 1610612736

def test_parse_size_edge_cases():
    assert parse_size('0 bytes') == 0
    assert parse_size('0') == 0
    assert parse_size('1 MB') == 1000000
    assert parse_size('1.0 TB') == 1000000000000
    assert parse_size('1.0 TB', binary=True) == 1099511627776
    assert parse_size('1 PB') == 1000000000000 * 1000
    assert parse_size('1.5 PB', binary=True) == 1125899906842624

def test_parse_size_invalid_cases():
    with pytest.raises(parse_size.InvalidSize):
        parse_size('not a size')
    with pytest.raises(parse_size.InvalidSize):
        parse_size('1.5 invalid_unit')
    with pytest.raises(parse_size.InvalidSize):
        parse_size('')
    with pytest.raises(parse_size.InvalidSize):
        parse_size('1.5')  # Ambiguous without a unit