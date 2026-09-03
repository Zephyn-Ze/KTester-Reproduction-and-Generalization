from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_mixed_proceedings_and_journal_records():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "Part A", "part_title": "First Proceedings", "paper_count": 5},
        {"year": 2021, "kind": "journal", "journal": "Journal of Testing", "volume": 10, "issue": 2, "paper_count": 3},
        {"year": 2022, "kind": "proceedings", "part": "Part B", "part_title": "Second Proceedings", "paper_count": 8}
    ]
    venue = "Conference A"
    
    expected_output = {
        "Conference A": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "Part A",
                    "display_name": "First Proceedings",
                    "paper_count": 5
                },
                {
                    "kind": "journal",
                    "journal": "Journal of Testing",
                    "display_name": "Journal of Testing volume 10 issue 2",
                    "volume": 10,
                    "issue": 2,
                    "paper_count": 3
                }
            ],
            2022: [
                {
                    "kind": "proceedings",
                    "part": "Part B",
                    "display_name": "Second Proceedings",
                    "paper_count": 8
                }
            ]
        }
    }
    
    assert generate_manifest_template(inventory, venue) == expected_output

def test_empty_inventory():
    inventory = []
    venue = "Conference B"
    
    expected_output = {
        "Conference B": {}
    }
    
    assert generate_manifest_template(inventory, venue) == expected_output

def test_multiple_records_for_same_year():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "Part A", "part_title": "Proceedings A", "paper_count": 1},
        {"year": 2021, "kind": "journal", "journal": "Journal A", "volume": 1, "issue": 1, "paper_count": 2},
        {"year": 2021, "kind": "journal", "journal": "Journal B", "volume": 2, "issue": 1, "paper_count": 3}
    ]
    venue = "Conference C"
    
    expected_output = {
        "Conference C": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "Part A",
                    "display_name": "Proceedings A",
                    "paper_count": 1
                },
                {
                    "kind": "journal",
                    "journal": "Journal A",
                    "display_name": "Journal A volume 1 issue 1",
                    "volume": 1,
                    "issue": 1,
                    "paper_count": 2
                },
                {
                    "kind": "journal",
                    "journal": "Journal B",
                    "display_name": "Journal B volume 2 issue 1",
                    "volume": 2,
                    "issue": 1,
                    "paper_count": 3
                }
            ]
        }
    }
    
    assert generate_manifest_template(inventory, venue) == expected_output

def test_boundary_year_values():
    inventory = [
        {"year": 2000, "kind": "journal", "journal": "Old Journal", "volume": 1, "issue": 1, "paper_count": 10},
        {"year": 2023, "kind": "proceedings", "part": "Part C", "part_title": "Recent Proceedings", "paper_count": 15}
    ]
    venue = "Conference D"
    
    expected_output = {
        "Conference D": {
            2000: [
                {
                    "kind": "journal",
                    "journal": "Old Journal",
                    "display_name": "Old Journal volume 1 issue 1",
                    "volume": 1,
                    "issue": 1,
                    "paper_count": 10
                }
            ],
            2023: [
                {
                    "kind": "proceedings",
                    "part": "Part C",
                    "display_name": "Recent Proceedings",
                    "paper_count": 15
                }
            ]
        }
    }
    
    assert generate_manifest_template(inventory, venue) == expected_output

def test_duplicate_records():
    inventory = [
        {"year": 2022, "kind": "proceedings", "part": "Part D", "part_title": "Duplicate Proceedings", "paper_count": 4},
        {"year": 2022, "kind": "proceedings", "part": "Part D", "part_title": "Duplicate Proceedings", "paper_count": 4}
    ]
    venue = "Conference E"
    
    expected_output = {
        "Conference E": {
            2022: [
                {
                    "kind": "proceedings",
                    "part": "Part D",
                    "display_name": "Duplicate Proceedings",
                    "paper_count": 4
                },
                {
                    "kind": "proceedings",
                    "part": "Part D",
                    "display_name": "Duplicate Proceedings",
                    "paper_count": 4
                }
            ]
        }
    }
    
    assert generate_manifest_template(inventory, venue) == expected_output

def test_record_with_missing_required_fields():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "Part E", "paper_count": 5},  # Missing part_title
        {"year": 2021, "kind": "journal", "journal": "Journal C", "paper_count": 2}  # Missing volume and issue
    ]
    venue = "Conference F"
    
    expected_output = {
        "Conference F": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "Part E",
                    "display_name": "None",  # Display name cannot be generated
                    "paper_count": 5
                }
            ]
        }
    }
    
    assert generate_manifest_template(inventory, venue) == expected_output

def test_record_with_invalid_kind():
    inventory = [
        {"year": 2021, "kind": "invalid_kind", "part": "Part F", "part_title": "Invalid Proceedings", "paper_count": 5}
    ]
    venue = "Conference G"
    
    expected_output = {
        "Conference G": {}
    }
    
    assert generate_manifest_template(inventory, venue) == expected_output

def test_large_inventory_processing():
    inventory = [{"year": 2021, "kind": "journal", "journal": f"Journal {i}", "volume": i, "issue": i, "paper_count": i} for i in range(1, 1001)]
    venue = "Conference H"
    
    expected_output = {
        "Conference H": {
            2021: [
                {
                    "kind": "journal",
                    "journal": f"Journal {i}",
                    "display_name": f"Journal {i} volume {i} issue {i}",
                    "volume": i,
                    "issue": i,
                    "paper_count": i
                } for i in range(1, 1001)
            ]
        }
    }
    
    assert generate_manifest_template(inventory, venue) == expected_output