from target_functions.parse_size_target import parse_size
import pytest

def test_parse_size_bytes():
    assert parse_size('42') == 42
    assert parse_size('13b') == 13
    assert parse_size('5 bytes') == 5

def test_parse_size_kilobytes():
    assert parse_size('1 KB') == 1000
    assert parse_size('1 kilobyte') == 1000
    assert parse_size('1.5 KB') == 1500

def test_parse_size_megabytes():
    assert parse_size('1 MB') == 1000000
    assert parse_size('1 megabyte') == 1000000
    assert parse_size('1.5 MB') == 1500000

def test_parse_size_gigabytes():
    assert parse_size('1 GB') == 1000000000
    assert parse_size('1 gigabyte') == 1000000000
    assert parse_size('1.5 GB') == 1500000000

def test_parse_size_terabytes():
    assert parse_size('1 TB') == 1000000000000
    assert parse_size('1 terabyte') == 1000000000000
    assert parse_size('1.5 TB') == 1500000000000

def test_parse_size_petabytes():
    assert parse_size('1 PB') == 1000000000000000
    assert parse_size('1 petabyte') == 1000000000000000
    assert parse_size('1.5 PB') == 1500000000000000

def test_parse_size_binary_kilobytes():
    assert parse_size('1 KiB', binary=True) == 1024
    assert parse_size('1 kibibyte', binary=True) == 1024
    assert parse_size('1.5 KiB', binary=True) == 1536

def test_parse_size_binary_megabytes():
    assert parse_size('1 MiB', binary=True) == 1048576
    assert parse_size('1 mebibyte', binary=True) == 1048576
    assert parse_size('1.5 MiB', binary=True) == 1572864

def test_parse_size_binary_gigabytes():
    assert parse_size('1 GiB', binary=True) == 1073741824
    assert parse_size('1 gibibyte', binary=True) == 1073741824
    assert parse_size('1.5 GiB', binary=True) == 1610612736

def test_parse_size_invalid():
    with pytest.raises(InvalidSize):
        parse_size('invalid input')
    with pytest.raises(InvalidSize):
        parse_size('')
    with pytest.raises(InvalidSize):
        parse_size('1.5 XYZ')