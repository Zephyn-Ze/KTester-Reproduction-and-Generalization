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
    assert parse_size('1 TB') == 1000000000000

def test_parse_size_edge_cases():
    assert parse_size('0') == 0
    assert parse_size('0 bytes') == 0
    assert parse_size('0 KB') == 0
    assert parse_size('0 MB') == 0
    assert parse_size('0 GB') == 0
    assert parse_size('0 TB') == 0
    assert parse_size('0 PB') == 0

def test_parse_size_invalid_cases():
    with pytest.raises(InvalidSize):
        parse_size('not a size')
    with pytest.raises(InvalidSize):
        parse_size('1.5 ZB')
    with pytest.raises(InvalidSize):
        parse_size('1.5 unknown')
    with pytest.raises(InvalidSize):
        parse_size('')

def test_parse_size_binary_cases():
    assert parse_size('1 KB', binary=True) == 1024
    assert parse_size('1 MiB') == 1048576
    assert parse_size('1 GiB', binary=True) == 1073741824
    assert parse_size('1 TiB', binary=True) == 1099511627776

def test_parse_size_large_numbers():
    assert parse_size('1 PB') == 1000000000000
    assert parse_size('1 EB') == 1000000000000000
    assert parse_size('1 ZB') == 1000000000000000000
    assert parse_size('1 YB') == 1000000000000000000000

def test_parse_size_float_values():
    assert parse_size('1.25 GB') == 1250000000
    assert parse_size('2.5 MB') == 2500000
    assert parse_size('0.5 TB') == 500000000000
    assert parse_size('0.1 PB') == 100000000000

def test_parse_size_with_spaces():
    assert parse_size('   1   KB   ') == 1000
    assert parse_size('  2.5   MB  ') == 2500000
    assert parse_size('  3    GiB  ') == 3221225472