import pytest
from target_functions.generate_manifest_template_target import generate_manifest_template

def test_generate_manifest_template_normal_cases():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "A", "part_title": "Conference A", "paper_count": 10},
        {"year": 2021, "kind": "journal", "journal": "Journal A", "volume": 1, "issue": 1, "paper_count": 5},
        {"year": 2022, "kind": "proceedings", "part": "B", "part_title": "Conference B", "paper_count": 15},
    ]
    venue = "Venue A"
    expected_output = {
        "Venue A": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "A",
                    "display_name": "Conference A",
                    "paper_count": 10,
                },
                {
                    "kind": "journal",
                    "journal": "Journal A",
                    "display_name": "Journal A volume 1 issue 1",
                    "volume": 1,
                    "issue": 1,
                    "paper_count": 5,
                },
            ],
            2022: [
                {
                    "kind": "proceedings",
                    "part": "B",
                    "display_name": "Conference B",
                    "paper_count": 15,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_empty_inventory():
    inventory = []
    venue = "Venue B"
    expected_output = {
        "Venue B": {}
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_single_record():
    inventory = [
        {"year": 2023, "kind": "journal", "journal": "Journal B", "volume": 2, "issue": 3, "paper_count": 8},
    ]
    venue = "Venue C"
    expected_output = {
        "Venue C": {
            2023: [
                {
                    "kind": "journal",
                    "journal": "Journal B",
                    "display_name": "Journal B volume 2 issue 3",
                    "volume": 2,
                    "issue": 3,
                    "paper_count": 8,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_multiple_years():
    inventory = [
        {"year": 2020, "kind": "proceedings", "part": "C", "part_title": "Conference C", "paper_count": 20},
        {"year": 2021, "kind": "proceedings", "part": "D", "part_title": "Conference D", "paper_count": 25},
        {"year": 2020, "kind": "journal", "journal": "Journal C", "volume": 3, "issue": 4, "paper_count": 12},
    ]
    venue = "Venue D"
    expected_output = {
        "Venue D": {
            2020: [
                {
                    "kind": "proceedings",
                    "part": "C",
                    "display_name": "Conference C",
                    "paper_count": 20,
                },
                {
                    "kind": "journal",
                    "journal": "Journal C",
                    "display_name": "Journal C volume 3 issue 4",
                    "volume": 3,
                    "issue": 4,
                    "paper_count": 12,
                },
            ],
            2021: [
                {
                    "kind": "proceedings",
                    "part": "D",
                    "display_name": "Conference D",
                    "paper_count": 25,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_case_years():
    inventory = [
        {"year": 1999, "kind": "proceedings", "part": "E", "part_title": "Conference E", "paper_count": 30},
        {"year": 2000, "kind": "journal", "journal": "Journal D", "volume": 4, "issue": 5, "paper_count": 18},
        {"year": 2025, "kind": "proceedings", "part": "F", "part_title": "Conference F", "paper_count": 40},
    ]
    venue = "Venue E"
    expected_output = {
        "Venue E": {
            1999: [
                {
                    "kind": "proceedings",
                    "part": "E",
                    "display_name": "Conference E",
                    "paper_count": 30,
                },
            ],
            2000: [
                {
                    "kind": "journal",
                    "journal": "Journal D",
                    "display_name": "Journal D volume 4 issue 5",
                    "volume": 4,
                    "issue": 5,
                    "paper_count": 18,
                },
            ],
            2025: [
                {
                    "kind": "proceedings",
                    "part": "F",
                    "display_name": "Conference F",
                    "paper_count": 40,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output