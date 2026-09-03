from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_generate_manifest_template_normal_cases():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "A", "part_title": "Part A Title", "paper_count": 10},
        {"year": 2021, "kind": "journal", "journal": "Journal A", "volume": 1, "issue": 1, "paper_count": 5},
        {"year": 2022, "kind": "proceedings", "part": "B", "part_title": "Part B Title", "paper_count": 8},
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
                    "volume": 1,
                    "issue": 1,
                    "paper_count": 5,
                },
            ],
            2022: [
                {
                    "kind": "proceedings",
                    "part": "B",
                    "display_name": "Part B Title",
                    "paper_count": 8,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_case_empty_inventory():
    inventory = []
    venue = "Conference B"
    expected_output = {
        "Conference B": {}
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_case_single_record():
    inventory = [
        {"year": 2023, "kind": "journal", "journal": "Journal B", "volume": 2, "issue": 3, "paper_count": 15},
    ]
    venue = "Conference C"
    expected_output = {
        "Conference C": {
            2023: [
                {
                    "kind": "journal",
                    "journal": "Journal B",
                    "display_name": "Journal B volume 2 issue 3",
                    "volume": 2,
                    "issue": 3,
                    "paper_count": 15,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_case_years_out_of_order():
    inventory = [
        {"year": 2022, "kind": "proceedings", "part": "C", "part_title": "Part C Title", "paper_count": 12},
        {"year": 2021, "kind": "journal", "journal": "Journal C", "volume": 3, "issue": 4, "paper_count": 20},
    ]
    venue = "Conference D"
    expected_output = {
        "Conference D": {
            2021: [
                {
                    "kind": "journal",
                    "journal": "Journal C",
                    "display_name": "Journal C volume 3 issue 4",
                    "volume": 3,
                    "issue": 4,
                    "paper_count": 20,
                },
            ],
            2022: [
                {
                    "kind": "proceedings",
                    "part": "C",
                    "display_name": "Part C Title",
                    "paper_count": 12,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_case_duplicate_years():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "D", "part_title": "Part D Title", "paper_count": 5},
        {"year": 2021, "kind": "journal", "journal": "Journal D", "volume": 4, "issue": 5, "paper_count": 10},
    ]
    venue = "Conference E"
    expected_output = {
        "Conference E": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "D",
                    "display_name": "Part D Title",
                    "paper_count": 5,
                },
                {
                    "kind": "journal",
                    "journal": "Journal D",
                    "display_name": "Journal D volume 4 issue 5",
                    "volume": 4,
                    "issue": 5,
                    "paper_count": 10,
                },
            ],
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output