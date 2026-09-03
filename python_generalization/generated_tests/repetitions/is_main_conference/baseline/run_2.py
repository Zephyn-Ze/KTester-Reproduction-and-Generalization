from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_is_main_conference_normal_cases():
    record1 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) is True

    record2 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "sigsoft/2023"}
    assert is_main_conference(record2, "FSE", {}) is True

    record3 = {"display_name": "Journal of Software Engineering", "kind": "journal", "issue": "Software Engineering"}
    assert is_main_conference(record3, "Software Engineering", {}) is True

def test_is_main_conference_edge_cases():
    record4 = {"display_name": "Companion Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record4, "ASE", {}) is False

    record5 = {"display_name": "Workshop on Software Engineering", "kind": "proceedings", "part": "sigsoft/2023"}
    assert is_main_conference(record5, "FSE", {}) is False

    record6 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023-1"}
    assert is_main_conference(record6, "ASE", {}) is True

    record7 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "unknown/2023"}
    assert is_main_conference(record7, "ASE", {}) is False

    record8 = {"display_name": "Journal of Software Engineering", "kind": "journal", "issue": "Software Engineering"}
    assert is_main_conference(record8, "software engineering", {}) is True

    record9 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record9, "Unknown Venue", {}) is False

    record10 = {"display_name": "International Conference on Software Engineering", "kind": "workshop", "part": "kbse/2023"}
    assert is_main_conference(record10, "ASE", {}) is False

def test_is_main_conference_case_insensitivity():
    record11 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "KBSE/2023"}
    assert is_main_conference(record11, "ase", {}) is True

    record12 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "sigsoft/2023"}
    assert is_main_conference(record12, "fse", {}) is True

    record13 = {"display_name": "Journal of Software Engineering", "kind": "journal", "issue": "software engineering"}
    assert is_main_conference(record13, "SOFTWARE ENGINEERING", {}) is True

    record14 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "unknown/2023"}
    assert is_main_conference(record14, "ASE", {}) is False

    record15 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record15, "ase", {}) is True