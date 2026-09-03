from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_generate_manifest_template_normal_cases():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "A", "part_title": "Conference A", "paper_count": 5},
        {"year": 2021, "kind": "journal", "journal": "Journal A", "volume": 1, "issue": 1, "paper_count": 10},
        {"year": 2022, "kind": "proceedings", "part": "B", "part_title": "Conference B", "paper_count": 3},
    ]
    venue = "Venue A"
    expected_output = {
        "Venue A": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "A",
                    "display_name": "Conference A",
                    "paper_count": 5,
                },
                {
                    "kind": "journal",
                    "journal": "Journal A",
                    "display_name": "Journal A volume 1 issue 1",
                    "volume": 1,
                    "issue": 1,
                    "paper_count": 10,
                },
            ],
            2022: [
                {
                    "kind": "proceedings",
                    "part": "B",
                    "display_name": "Conference B",
                    "paper_count": 3,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_cases():
    # Test with empty inventory
    inventory = []
    venue = "Venue B"
    expected_output = {"Venue B": {}}
    assert generate_manifest_template(inventory, venue) == expected_output

    # Test with one record of each kind
    inventory = [
        {"year": 2023, "kind": "proceedings", "part": "C", "part_title": "Conference C", "paper_count": 2},
        {"year": 2023, "kind": "journal", "journal": "Journal B", "volume": 2, "issue": 2, "paper_count": 4},
    ]
    venue = "Venue C"
    expected_output = {
        "Venue C": {
            2023: [
                {
                    "kind": "proceedings",
                    "part": "C",
                    "display_name": "Conference C",
                    "paper_count": 2,
                },
                {
                    "kind": "journal",
                    "journal": "Journal B",
                    "display_name": "Journal B volume 2 issue 2",
                    "volume": 2,
                    "issue": 2,
                    "paper_count": 4,
                },
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

    # Test with multiple years and mixed kinds
    inventory = [
        {"year": 2021, "kind": "journal", "journal": "Journal C", "volume": 3, "issue": 1, "paper_count": 1},
        {"year": 2021, "kind": "proceedings", "part": "D", "part_title": "Conference D", "paper_count": 0},
        {"year": 2022, "kind": "journal", "journal": "Journal D", "volume": 4, "issue": 2, "paper_count": 2},
    ]
    venue = "Venue D"
    expected_output = {
        "Venue D": {
            2021: [
                {
                    "kind": "journal",
                    "journal": "Journal C",
                    "display_name": "Journal C volume 3 issue 1",
                    "volume": 3,
                    "issue": 1,
                    "paper_count": 1,
                },
                {
                    "kind": "proceedings",
                    "part": "D",
                    "display_name": "Conference D",
                    "paper_count": 0,
                },
            ],
            2022: [
                {
                    "kind": "journal",
                    "journal": "Journal D",
                    "display_name": "Journal D volume 4 issue 2",
                    "volume": 4,
                    "issue": 2,
                    "paper_count": 2,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output