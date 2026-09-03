from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_excluded_words_in_display_name():
    record = {
        "display_name": "Workshop on AI",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "AI Conference"
    }
    venue = "AI Conference"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_kind_is_proceedings_with_valid_url_format():
    record = {
        "display_name": "Main Conference on Software Engineering",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_kind_is_proceedings_with_invalid_url_format():
    record = {
        "display_name": "Software Engineering Conference",
        "kind": "proceedings",
        "part": "ase/2023/extra",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_kind_is_not_proceedings_and_venue_matches_issue():
    record = {
        "display_name": "Annual Software Engineering Symposium",
        "kind": "symposium",
        "part": "",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_kind_is_not_proceedings_and_venue_does_not_match_issue():
    record = {
        "display_name": "Annual Software Engineering Symposium",
        "kind": "symposium",
        "part": "",
        "issue": "ASE"
    }
    venue = "ICSE"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_case_insensitive_venue_and_issue_match():
    record = {
        "display_name": "Software Engineering Conference",
        "kind": "symposium",
        "part": "",
        "issue": "ase"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_missing_key_in_record():
    record = {
        "display_name": "Main Conference",
        "kind": "proceedings",
        "part": "ase/2023"
        # Missing 'issue' key
    }
    venue = "ASE"
    config = {}
    with pytest.raises(KeyError):
        is_main_conference(record, venue, config)

def test_boundary_case_with_empty_display_name():
    record = {
        "display_name": "",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "ASE"
    }
    venue = "ASE"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_duplicate_words_in_display_name():
    record = {
        "display_name": "Demo Demo Conference",
        "kind": "proceedings",
        "part": "sigsoft/2023",
        "issue": "SIGSOFT"
    }
    venue = "SIGSOFT"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_valid_kind_with_unmatched_venue_and_issue():
    record = {
        "display_name": "International Conference on Software Engineering",
        "kind": "workshop",
        "part": "",
        "issue": "ASE"
    }
    venue = "ICSE"
    config = {}
    assert is_main_conference(record, venue, config) is False