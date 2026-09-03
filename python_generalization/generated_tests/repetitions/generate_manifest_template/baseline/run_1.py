from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_generate_manifest_template_normal_cases():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "A", "part_title": "Part A Title", "paper_count": 10},
        {"year": 2021, "kind": "journal", "journal": "Journal A", "volume": "1", "issue": "1", "paper_count": 5},
        {"year": 2022, "kind": "journal", "journal": "Journal B", "volume": "2", "issue": "1", "paper_count": 3},
    ]
    venue = "Conference A"
    expected_output = {
        "Conference A": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "A",
                    "display_name": "Part A Title",
                    "paper_count": 10,
                },
                {
                    "kind": "journal",
                    "journal": "Journal A",
                    "display_name": "Journal A volume 1 issue 1",
                    "volume": "1",
                    "issue": "1",
                    "paper_count": 5,
                },
            ],
            2022: [
                {
                    "kind": "journal",
                    "journal": "Journal B",
                    "display_name": "Journal B volume 2 issue 1",
                    "volume": "2",
                    "issue": "1",
                    "paper_count": 3,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_case_empty_inventory():
    inventory = []
    venue = "Conference A"
    expected_output = {
        "Conference A": {}
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_single_entry_proceedings():
    inventory = [
        {"year": 2023, "kind": "proceedings", "part": "B", "part_title": "Part B Title", "paper_count": 8},
    ]
    venue = "Conference B"
    expected_output = {
        "Conference B": {
            2023: [
                {
                    "kind": "proceedings",
                    "part": "B",
                    "display_name": "Part B Title",
                    "paper_count": 8,
                },
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_multiple_years():
    inventory = [
        {"year": 2020, "kind": "journal", "journal": "Journal C", "volume": "3", "issue": "2", "paper_count": 2},
        {"year": 2021, "kind": "journal", "journal": "Journal D", "volume": "4", "issue": "3", "paper_count": 4},
        {"year": 2020, "kind": "proceedings", "part": "C", "part_title": "Part C Title", "paper_count": 6},
    ]
    venue = "Conference C"
    expected_output = {
        "Conference C": {
            2020: [
                {
                    "kind": "journal",
                    "journal": "Journal C",
                    "display_name": "Journal C volume 3 issue 2",
                    "volume": "3",
                    "issue": "2",
                    "paper_count": 2,
                },
                {
                    "kind": "proceedings",
                    "part": "C",
                    "display_name": "Part C Title",
                    "paper_count": 6,
                },
            ],
            2021: [
                {
                    "kind": "journal",
                    "journal": "Journal D",
                    "display_name": "Journal D volume 4 issue 3",
                    "volume": "4",
                    "issue": "3",
                    "paper_count": 4,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_different_kinds_same_year():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "D", "part_title": "Part D Title", "paper_count": 1},
        {"year": 2021, "kind": "journal", "journal": "Journal E", "volume": "5", "issue": "4", "paper_count": 7},
    ]
    venue = "Conference D"
    expected_output = {
        "Conference D": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "D",
                    "display_name": "Part D Title",
                    "paper_count": 1,
                },
                {
                    "kind": "journal",
                    "journal": "Journal E",
                    "display_name": "Journal E volume 5 issue 4",
                    "volume": "5",
                    "issue": "4",
                    "paper_count": 7,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output