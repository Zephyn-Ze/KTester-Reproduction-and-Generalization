from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_is_main_conference_normal_cases():
    record1 = {"display_name": "Main Conference 2023", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) is True

    record2 = {"display_name": "Another Main Conference", "kind": "journal", "issue": "another main conference"}
    assert is_main_conference(record2, "Another Main Conference", {}) is True

def test_is_main_conference_exclude_cases():
    record1 = {"display_name": "Workshop on AI", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) is False

    record2 = {"display_name": "Demo Session", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record2, "ASE", {}) is False

def test_is_main_conference_proceedings_with_stream_mapping():
    record = {"display_name": "Conference on Software Engineering", "kind": "proceedings", "part": "sigsoft/2023"}
    assert is_main_conference(record, "FSE", {}) is True

def test_is_main_conference_invalid_proceedings():
    record = {"display_name": "Conference on Software Engineering", "kind": "proceedings", "part": "invalid/2023"}
    assert is_main_conference(record, "FSE", {}) is False

def test_is_main_conference_edge_cases():
    record1 = {"display_name": "", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) is False

    record2 = {"display_name": "Conference", "kind": "journal", "issue": ""}
    assert is_main_conference(record2, "", {}) is False

    record3 = {"display_name": "Main Conference", "kind": "proceedings", "part": "kbse/2023-1"}
    assert is_main_conference(record3, "ASE", {}) is True

    record4 = {"display_name": "Main Conference", "kind": "proceedings", "part": "kbse/2023-01"}
    assert is_main_conference(record4, "ASE", {}) is True

    record5 = {"display_name": "Main Conference", "kind": "proceedings", "part": "kbse/2023-01-01"}
    assert is_main_conference(record5, "ASE", {}) is False

    record6 = {"display_name": "Main Conference", "kind": "unknown", "issue": "Main Conference"}
    assert is_main_conference(record6, "Main Conference", {}) is True

    record7 = {"display_name": "Companion Event", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record7, "ASE", {}) is False