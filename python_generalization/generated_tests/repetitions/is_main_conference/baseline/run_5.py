from target_functions.is_main_conference_target import is_main_conference
import pytest

def test_is_main_conference_normal_cases():
    record1 = {"display_name": "International Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) == True

    record2 = {"display_name": "Annual Symposium on Programming Languages", "kind": "journal", "issue": "programming languages"}
    assert is_main_conference(record2, "programming languages", {}) == True

def test_is_main_conference_excluded_words():
    record1 = {"display_name": "Demo of New Software", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record1, "ASE", {}) == False

    record2 = {"display_name": "Workshop on AI", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record2, "ASE", {}) == False

def test_is_main_conference_proceedings_with_stream_mapping():
    record1 = {"display_name": "Conference on Software Engineering", "kind": "proceedings", "part": "fse/2022"}
    assert is_main_conference(record1, "FSE", {}) == True

    record2 = {"display_name": "Conference on Software Engineering", "kind": "proceedings", "part": "other/2022"}
    assert is_main_conference(record2, "FSE", {}) == False

def test_is_main_conference_edge_cases():
    record1 = {"display_name": "Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023-1"}
    assert is_main_conference(record1, "ASE", {}) == True

    record2 = {"display_name": "Conference on Software Engineering", "kind": "proceedings", "part": "kbse/2023-abc"}
    assert is_main_conference(record2, "ASE", {}) == False

    record3 = {"display_name": "Conference on Software Engineering", "kind": "journal", "issue": "ASE"}
    assert is_main_conference(record3, "ASE", {}) == True

    record4 = {"display_name": "Conference on Software Engineering", "kind": "journal", "issue": "other"}
    assert is_main_conference(record4, "ASE", {}) == False

    record5 = {"display_name": "Companion to the Conference", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record5, "ASE", {}) == False

    record6 = {"display_name": "Tutorial on Software Engineering", "kind": "proceedings", "part": "kbse/2023"}
    assert is_main_conference(record6, "ASE", {}) == False