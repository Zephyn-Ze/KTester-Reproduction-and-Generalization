from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_normal_case_with_mixed_records():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "1", "part_title": "Opening", "paper_count": 5},
        {"year": 2021, "kind": "journal", "journal": "Journal A", "volume": "10", "issue": "1", "paper_count": 3},
        {"year": 2022, "kind": "proceedings", "part": "2", "part_title": "Closing", "paper_count": 4}
    ]
    venue = "Conference XYZ"
    expected = {
        "Conference XYZ": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "1",
                    "display_name": "Opening",
                    "paper_count": 5
                },
                {
                    "kind": "journal",
                    "journal": "Journal A",
                    "display_name": "Journal A volume 10 issue 1",
                    "volume": "10",
                    "issue": "1",
                    "paper_count": 3
                }
            ],
            2022: [
                {
                    "kind": "proceedings",
                    "part": "2",
                    "display_name": "Closing",
                    "paper_count": 4
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected

def test_empty_inventory():
    inventory = []
    venue = "Conference XYZ"
    expected = {
        "Conference XYZ": {}
    }
    assert generate_manifest_template(inventory, venue) == expected

def test_all_records_in_same_year():
    inventory = [
        {"year": 2021, "kind": "journal", "journal": "Journal B", "volume": "5", "issue": "2", "paper_count": 10},
        {"year": 2021, "kind": "proceedings", "part": "3", "part_title": "Session A", "paper_count": 2}
    ]
    venue = "Conference ABC"
    expected = {
        "Conference ABC": {
            2021: [
                {
                    "kind": "journal",
                    "journal": "Journal B",
                    "display_name": "Journal B volume 5 issue 2",
                    "volume": "5",
                    "issue": "2",
                    "paper_count": 10
                },
                {
                    "kind": "proceedings",
                    "part": "3",
                    "display_name": "Session A",
                    "paper_count": 2
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected

def test_duplicate_records():
    inventory = [
        {"year": 2021, "kind": "journal", "journal": "Journal C", "volume": "1", "issue": "1", "paper_count": 5},
        {"year": 2021, "kind": "journal", "journal": "Journal C", "volume": "1", "issue": "1", "paper_count": 5}
    ]
    venue = "Conference DEF"
    expected = {
        "Conference DEF": {
            2021: [
                {
                    "kind": "journal",
                    "journal": "Journal C",
                    "display_name": "Journal C volume 1 issue 1",
                    "volume": "1",
                    "issue": "1",
                    "paper_count": 5
                },
                {
                    "kind": "journal",
                    "journal": "Journal C",
                    "display_name": "Journal C volume 1 issue 1",
                    "volume": "1",
                    "issue": "1",
                    "paper_count": 5
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected

def test_boundary_case_with_missing_keys():
    inventory = [
        {"year": 2021, "kind": "journal", "volume": "1", "issue": "1", "paper_count": 5},
        {"year": 2021, "kind": "proceedings", "part": "1", "part_title": "Intro", "paper_count": 2}
    ]
    venue = "Conference GHI"
    with pytest.raises(KeyError):
        generate_manifest_template(inventory, venue)

def test_invalid_kind_value():
    inventory = [
        {"year": 2021, "kind": "invalid_kind", "journal": "Journal D", "volume": "2", "issue": "1", "paper_count": 5}
    ]
    venue = "Conference JKL"
    expected = {
        "Conference JKL": {
            2021: [
                {
                    "kind": "invalid_kind",
                    "journal": "Journal D",
                    "display_name": "Journal D volume 2 issue 1",
                    "volume": "2",
                    "issue": "1",
                    "paper_count": 5
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected