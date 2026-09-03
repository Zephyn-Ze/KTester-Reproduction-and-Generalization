from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_exclusion_of_companion_conference():
    record = {
        "display_name": "Companion Conference on Software Engineering",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_valid_proceedings_with_regex_match():
    record = {
        "display_name": "Annual Software Engineering Conference",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_proceedings_with_non_matching_regex():
    record = {
        "display_name": "Annual Software Engineering Conference",
        "kind": "proceedings",
        "part": "ase/2023-1",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_non_proceedings_kind():
    record = {
        "display_name": "Annual Software Engineering Conference",
        "kind": "workshop",
        "part": "ase/2023",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_case_insensitive_venue_and_issue_match():
    record = {
        "display_name": "Annual Software Engineering Conference",
        "kind": "workshop",
        "part": "ase/2023",
        "issue": "ase"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_no_exclusion_words_in_display_name():
    record = {
        "display_name": "International Conference on Software Engineering",
        "kind": "proceedings",
        "part": "fse/2023",
        "issue": "FSE"
    }
    venue = "FSE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_missing_key_in_record():
    record = {
        "display_name": "Conference on Software Engineering",
        "kind": "proceedings",
        "part": "ase/2023"
    }
    venue = "ASE"
    config = {}
    with pytest.raises(KeyError):
        is_main_conference(record, venue, config)

def test_empty_strings_for_record_keys():
    record = {
        "display_name": "",
        "kind": "",
        "part": "",
        "issue": ""
    }
    venue = ""
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_duplicate_display_name():
    record = {
        "display_name": "Annual Software Engineering Conference",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_invalid_data_types():
    record = {
        "display_name": 123,
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    with pytest.raises(TypeError):
        is_main_conference(record, venue, config)