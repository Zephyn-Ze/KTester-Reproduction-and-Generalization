from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_generate_manifest_template_normal_cases():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "A", "part_title": "Proceedings A", "paper_count": 10},
        {"year": 2021, "kind": "journal", "journal": "Journal A", "volume": 1, "issue": 1, "paper_count": 5},
        {"year": 2022, "kind": "proceedings", "part": "B", "part_title": "Proceedings B", "paper_count": 15}
    ]
    venue = "Conference A"
    expected_output = {
        "Conference A": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "A",
                    "display_name": "Proceedings A",
                    "paper_count": 10
                },
                {
                    "kind": "journal",
                    "journal": "Journal A",
                    "display_name": "Journal A volume 1 issue 1",
                    "volume": 1,
                    "issue": 1,
                    "paper_count": 5
                }
            ],
            2022: [
                {
                    "kind": "proceedings",
                    "part": "B",
                    "display_name": "Proceedings B",
                    "paper_count": 15
                }
            ]
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
        {"year": 2023, "kind": "journal", "journal": "Journal B", "volume": 2, "issue": 2, "paper_count": 3}
    ]
    venue = "Conference C"
    expected_output = {
        "Conference C": {
            2023: [
                {
                    "kind": "journal",
                    "journal": "Journal B",
                    "display_name": "Journal B volume 2 issue 2",
                    "volume": 2,
                    "issue": 2,
                    "paper_count": 3
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_case_same_year_different_kinds():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "C", "part_title": "Proceedings C", "paper_count": 8},
        {"year": 2021, "kind": "journal", "journal": "Journal C", "volume": 3, "issue": 3, "paper_count": 4}
    ]
    venue = "Conference D"
    expected_output = {
        "Conference D": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "C",
                    "display_name": "Proceedings C",
                    "paper_count": 8
                },
                {
                    "kind": "journal",
                    "journal": "Journal C",
                    "display_name": "Journal C volume 3 issue 3",
                    "volume": 3,
                    "issue": 3,
                    "paper_count": 4
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_generate_manifest_template_edge_case_multiple_years():
    inventory = [
        {"year": 2020, "kind": "proceedings", "part": "D", "part_title": "Proceedings D", "paper_count": 12},
        {"year": 2021, "kind": "proceedings", "part": "E", "part_title": "Proceedings E", "paper_count": 6},
        {"year": 2020, "kind": "journal", "journal": "Journal D", "volume": 4, "issue": 4, "paper_count": 2},
        {"year": 2021, "kind": "journal", "journal": "Journal E", "volume": 5, "issue": 5, "paper_count": 1}
    ]
    venue = "Conference E"
    expected_output = {
        "Conference E": {
            2020: [
                {
                    "kind": "proceedings",
                    "part": "D",
                    "display_name": "Proceedings D",
                    "paper_count": 12
                },
                {
                    "kind": "journal",
                    "journal": "Journal D",
                    "display_name": "Journal D volume 4 issue 4",
                    "volume": 4,
                    "issue": 4,
                    "paper_count": 2
                }
            ],
            2021: [
                {
                    "kind": "proceedings",
                    "part": "E",
                    "display_name": "Proceedings E",
                    "paper_count": 6
                },
                {
                    "kind": "journal",
                    "journal": "Journal E",
                    "display_name": "Journal E volume 5 issue 5",
                    "volume": 5,
                    "issue": 5,
                    "paper_count": 1
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output