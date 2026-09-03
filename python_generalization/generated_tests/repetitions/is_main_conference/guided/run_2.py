from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_excluded_word_in_display_name():
    record = {
        "display_name": "International Workshop on AI",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "AI Conference"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_valid_proceedings_with_correct_url_format():
    record = {
        "display_name": "Main Conference on Software Engineering",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "Software Engineering"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_proceedings_with_incorrect_url_format():
    record = {
        "display_name": "Main Conference on Software Engineering",
        "kind": "proceedings",
        "part": "ase/2023/extra",
        "issue": "Software Engineering"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_non_proceedings_kind():
    record = {
        "display_name": "Annual Conference on AI",
        "kind": "workshop",
        "part": "ai/2023",
        "issue": "AI Conference"
    }
    venue = "AI Conference"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_matching_venue_and_issue():
    record = {
        "display_name": "Annual Conference on AI",
        "kind": "non-proceedings",
        "part": "ai/2023",
        "issue": "AI Conference"
    }
    venue = "AI Conference"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_case_insensitivity():
    record = {
        "display_name": "Main Conference on Software Engineering",
        "kind": "proceedings",
        "part": "ASE/2023",
        "issue": "software engineering"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is True

def test_empty_display_name():
    record = {
        "display_name": "",
        "kind": "proceedings",
        "part": "ase/2023",
        "issue": "Software Engineering"
    }
    venue = "ase"
    config = {}
    assert is_main_conference(record, venue, config) is False

def test_missing_keys_in_record():
    record = {
        "display_name": "Conference on AI",
        "kind": "proceedings",
        "part": "ai/2023"
        # Missing 'issue' key
    }
    venue = "ai"
    config = {}
    with pytest.raises(KeyError):
        is_main_conference(record, venue, config)

def test_invalid_venue_type():
    record = {
        "display_name": "Conference on AI",
        "kind": "proceedings",
        "part": "ai/2023",
        "issue": "AI Conference"
    }
    venue = None  # Invalid type
    config = {}
    with pytest.raises(TypeError):
        is_main_conference(record, venue, config)

def test_duplicate_excluded_words():
    record = {
        "display_name": "Workshop Workshop on AI",
        "kind": "proceedings",
        "part": "ai/2023",
        "issue": "AI Conference"
    }
    venue = "ai"
    config = {}
    assert is_main_conference(record, venue, config) is False