from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_excluded_word_in_display_name():
    record = {
        "display_name": "Workshop on AI",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "AI Conference"
    }
    venue = "AI Conference"
    config = {}
    assert is_main_conference(record, venue, config) == False

def test_valid_proceedings_record():
    record = {
        "display_name": "Main Conference on Software Engineering",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "Software Engineering"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) == True

def test_proceedings_record_with_invalid_part():
    record = {
        "display_name": "Main Conference on Software Engineering",
        "kind": "proceedings",
        "part": "invalid_part",
        "issue": "Software Engineering"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) == False

def test_non_proceedings_record_with_matching_venue_and_issue():
    record = {
        "display_name": "Special Session on AI",
        "kind": "session",
        "part": "some_part",
        "issue": "AI Conference"
    }
    venue = "AI Conference"
    config = {}
    assert is_main_conference(record, venue, config) == True

def test_non_proceedings_record_with_non_matching_venue_and_issue():
    record = {
        "display_name": "Special Session on AI",
        "kind": "session",
        "part": "some_part",
        "issue": "Data Science Conference"
    }
    venue = "AI Conference"
    config = {}
    assert is_main_conference(record, venue, config) == False

def test_empty_display_name():
    record = {
        "display_name": "",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "Software Engineering"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) == False

def test_case_sensitivity_in_venue_and_issue():
    record = {
        "display_name": "Conference on Software Engineering",
        "kind": "session",
        "part": "some_part",
        "issue": "software engineering"
    }
    venue = "Software Engineering"
    config = {}
    assert is_main_conference(record, venue, config) == True

def test_missing_key_in_record():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        # "part" is missing
        "issue": "Main Conference"
    }
    venue = "Main Conference"
    config = {}
    with pytest.raises(KeyError):
        is_main_conference(record, venue, config)

def test_invalid_data_types():
    record = {
        "display_name": 12345,  # Invalid type
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "Software Engineering"
    }
    venue = "ASE"
    config = {}
    with pytest.raises(TypeError):
        is_main_conference(record, venue, config)

def test_edge_case_with_whitespace_strings():
    record = {
        "display_name": "   ",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "   "
    }
    venue = "   "
    config = {}
    assert is_main_conference(record, venue, config) == False