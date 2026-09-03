from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_excluded_name():
    record = {
        "display_name": "Companion Event",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "2023"
    }
    venue = "Some Venue"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_valid_proceedings():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "2023"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_invalid_proceedings_no_match():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "some/other/format",
        "issue": "2023"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_non_proceedings_match():
    record = {
        "display_name": "Another Conference",
        "kind": "workshop",
        "part": "irrelevant",
        "issue": "Some Venue"
    }
    venue = "Some Venue"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_non_matching_venue():
    record = {
        "display_name": "Another Conference",
        "kind": "workshop",
        "part": "irrelevant",
        "issue": "Different Venue"
    }
    venue = "Some Venue"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_case_insensitivity():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "fse/2023",
        "issue": "FSE"
    }
    venue = "fse"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_empty_display_name():
    record = {
        "display_name": "",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "2023"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_missing_record_keys():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings"
        # Missing "part" and "issue"
    }
    venue = "ASE"
    config = {}
    with pytest.raises(KeyError):
        is_main_conference(record, venue, config)

def test_special_characters_in_display_name():
    record = {
        "display_name": "Main Conference @ 2023!",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "2023"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_duplicate_venue_case():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "fse/2023",
        "issue": "FSE"
    }
    venue = "FSE"
    config = {}
    assert is_main_conference(record, venue, config) is True