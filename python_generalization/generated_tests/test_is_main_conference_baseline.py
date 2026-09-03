from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_is_main_conference_normal_cases():
    record_1 = {"display_name": "Main Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record_1, "ASE", {}) is True

    record_2 = {"display_name": "Annual Meeting", "kind": "journal", "issue": "annual meeting"}
    assert is_main_conference(record_2, "Annual Meeting", {}) is True

    record_3 = {"display_name": "Software Engineering Workshop", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record_3, "ASE", {}) is False

def test_is_main_conference_edge_cases():
    record_4 = {"display_name": "Demo Session", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record_4, "ASE", {}) is False

    record_5 = {"display_name": "Tutorial on Software Testing", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record_5, "ASE", {}) is False

    record_6 = {"display_name": "Main Conference on Software Engineering", "kind": "proceedings", "part": "fse/2023"}
    assert is_main_conference(record_6, "FSE", {}) is True

    record_7 = {"display_name": "Conference Proceedings", "kind": "proceedings", "part": "unknown/2023"}
    assert is_main_conference(record_7, "Unknown", {}) is False

    record_8 = {"display_name": "Annual Conference", "kind": "journal", "issue": "Annual Conference"}
    assert is_main_conference(record_8, "Annual Conference", {}) is True

    record_9 = {"display_name": "Conference on AI", "kind": "proceedings", "part": "ai/2023"}
    assert is_main_conference(record_9, "AI", {}) is True

    record_10 = {"display_name": "Non-Main Event", "kind": "proceedings", "part": "kbse/2023", "issue": "non-main"}
    assert is_main_conference(record_10, "Non-Main", {}) is False

def test_is_main_conference_case_insensitivity():
    record_11 = {"display_name": "Main Conference", "kind": "proceedings", "part": "KBSE/2022"}
    assert is_main_conference(record_11, "kbse", {}) is True

    record_12 = {"display_name": "Main Conference", "kind": "journal", "issue": "MAIN CONFERENCE"}
    assert is_main_conference(record_12, "main conference", {}) is True

    record_13 = {"display_name": "Conference on Testing", "kind": "proceedings", "part": "fse/2022"}
    assert is_main_conference(record_13, "FSE", {}) is True

    record_14 = {"display_name": "Demo", "kind": "proceedings", "part": "fse/2022"}
    assert is_main_conference(record_14, "FSE", {}) is False

    record_15 = {"display_name": "WORKSHOP", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record_15, "ASE", {}) is False