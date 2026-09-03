from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_is_main_conference_normal_cases():
    record1 = {"display_name": "Main Conference 2023", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) is True

    record2 = {"display_name": "Main Conference 2023", "kind": "proceedings", "part": "sigsoft/2023"}
    assert is_main_conference(record2, "FSE", {}) is True

    record3 = {"display_name": "Another Conference", "kind": "journal", "issue": "Another Conference"}
    assert is_main_conference(record3, "Another Conference", {}) is True

def test_is_main_conference_edge_cases():
    record4 = {"display_name": "Workshop on AI", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record4, "ASE", {}) is False

    record5 = {"display_name": "Demo Conference", "kind": "proceedings", "part": "sigsoft/2023"}
    assert is_main_conference(record5, "FSE", {}) is False

    record6 = {"display_name": "Main Conference 2023", "kind": "proceedings", "part": "kbse/2022"}
    assert is_main_conference(record6, "ASE", {}) is False

    record7 = {"display_name": "Main Conference 2023", "kind": "proceedings", "part": "kbse/2023-1"}
    assert is_main_conference(record7, "ASE", {}) is True

    record8 = {"display_name": "Main Conference 2023", "kind": "journal", "issue": "Different Issue"}
    assert is_main_conference(record8, "Different Issue", {}) is False

def test_is_main_conference_case_insensitivity():
    record9 = {"display_name": "Main Conference 2023", "kind": "proceedings", "part": "KBSE/2023"}
    assert is_main_conference(record9, "ase", {}) is True

    record10 = {"display_name": "Main Conference 2023", "kind": "proceedings", "part": "SIGSOFT/2023"}
    assert is_main_conference(record10, "fse", {}) is True

def test_is_main_conference_empty_record():
    record11 = {}
    assert is_main_conference(record11, "ASE", {}) is False

def test_is_main_conference_missing_keys():
    record12 = {"display_name": "Main Conference 2023"}
    assert is_main_conference(record12, "ASE", {}) is False

    record13 = {"kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record13, "ASE", {}) is False