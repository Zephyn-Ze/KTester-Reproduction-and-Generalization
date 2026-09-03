from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_is_main_conference_normal_cases():
    record1 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) is True

    record2 = {"display_name": "Annual Symposium on Programming Languages", "kind": "journal", "issue": "programming languages"}
    assert is_main_conference(record2, "programming languages", {}) is True

def test_is_main_conference_exclude_cases():
    record1 = {"display_name": "Demo of New Software", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) is False

    record2 = {"display_name": "Workshop on AI", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record2, "ASE", {}) is False

def test_is_main_conference_edge_cases():
    record1 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "fse/2023"}
    assert is_main_conference(record1, "FSE", {}) is True

    record2 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023-1"}
    assert is_main_conference(record2, "ASE", {}) is True

    record3 = {"display_name": "Some Other Conference", "kind": "journal", "issue": "different issue"}
    assert is_main_conference(record3, "Some Venue", {}) is False

    record4 = {"display_name": "Some Conference", "kind": "proceedings", "part": "unknown/2023"}
    assert is_main_conference(record4, "Unknown", {}) is False

    record5 = {"display_name": "Conference with No Year", "kind": "proceedings", "part": "kbse/2023-"}
    assert is_main_conference(record5, "ASE", {}) is False

    record6 = {"display_name": "Conference with No Year", "kind": "proceedings", "part": "kbse/2023-abc"}
    assert is_main_conference(record6, "ASE", {}) is False

    record7 = {"display_name": "Conference with Issue", "kind": "journal", "issue": "same issue"}
    assert is_main_conference(record7, "SAME ISSUE", {}) is True

    record8 = {"display_name": "Non-Matching Conference", "kind": "proceedings", "part": "fse/2023"}
    assert is_main_conference(record8, "ASE", {}) is False

    record9 = {"display_name": "Proceedings of a Workshop", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record9, "ASE", {}) is False