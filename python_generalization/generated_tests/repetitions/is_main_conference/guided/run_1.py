from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_excluded_conference_type():
    record = {
        "display_name": "Companion Conference",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ase"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_valid_proceedings_conference_with_matching_url():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ase"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_proceedings_conference_with_non_matching_url():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "fse/2022",
        "issue": "ase"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_non_proceedings_type_with_matching_venue():
    record = {
        "display_name": "Some Conference",
        "kind": "symposium",
        "part": "n/a",
        "issue": "Main Venue"
    }
    venue = "Main Venue"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_non_proceedings_type_with_non_matching_venue():
    record = {
        "display_name": "Some Conference",
        "kind": "symposium",
        "part": "n/a",
        "issue": "Different Venue"
    }
    venue = "Main Venue"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_case_sensitivity_in_venue_and_issue():
    record = {
        "display_name": "Some Conference",
        "kind": "symposium",
        "part": "n/a",
        "issue": "lowercase venue"
    }
    venue = "Lowercase Venue"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_boundary_case_with_empty_display_name():
    record = {
        "display_name": "",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ase"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_boundary_case_with_empty_venue():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ase"
    }
    venue = ""
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_keyerror_due_to_missing_key_in_record():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "ase/2023"
        # Missing 'issue' key
    }
    venue = "ase"
    config = {}
    with pytest.raises(KeyError):
        is_main_conference(record, venue, config)

def test_typeerror_due_to_non_string_input():
    record = {
        "display_name": None,  # Invalid type
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ase"
    }
    venue = "ase"
    config = {}
    with pytest.raises(TypeError):
        is_main_conference(record, venue, config)