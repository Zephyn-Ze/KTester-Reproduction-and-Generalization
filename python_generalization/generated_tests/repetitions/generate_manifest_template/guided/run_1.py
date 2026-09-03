from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_mixed_record_types():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "Part A", "part_title": "Proceedings of Part A", "paper_count": 5},
        {"year": 2021, "kind": "journal", "journal": "Journal of Testing", "volume": 10, "issue": 1, "paper_count": 3},
        {"year": 2022, "kind": "proceedings", "part": "Part B", "part_title": "Proceedings of Part B", "paper_count": 8}
    ]
    venue = "Conference XYZ"
    expected_output = {
        "Conference XYZ": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "Part A",
                    "display_name": "Proceedings of Part A",
                    "paper_count": 5,
                },
                {
                    "kind": "journal",
                    "journal": "Journal of Testing",
                    "display_name": "Journal of Testing volume 10 issue 1",
                    "volume": 10,
                    "issue": 1,
                    "paper_count": 3,
                }
            ],
            2022: [
                {
                    "kind": "proceedings",
                    "part": "Part B",
                    "display_name": "Proceedings of Part B",
                    "paper_count": 8,
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_empty_inventory():
    inventory = []
    venue = "Conference XYZ"
    expected_output = {
        "Conference XYZ": {}
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_duplicate_years():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "Part A", "part_title": "Proceedings of Part A", "paper_count": 5},
        {"year": 2021, "kind": "journal", "journal": "Journal of Testing", "volume": 10, "issue": 1, "paper_count": 3}
    ]
    venue = "Conference XYZ"
    expected_output = {
        "Conference XYZ": {
            2021: [
                {
                    "kind": "proceedings",
                    "part": "Part A",
                    "display_name": "Proceedings of Part A",
                    "paper_count": 5,
                },
                {
                    "kind": "journal",
                    "journal": "Journal of Testing",
                    "display_name": "Journal of Testing volume 10 issue 1",
                    "volume": 10,
                    "issue": 1,
                    "paper_count": 3,
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_year_as_string():
    inventory = [
        {"year": "2021", "kind": "proceedings", "part": "Part A", "part_title": "Proceedings of Part A", "paper_count": 5},
        {"year": "2021", "kind": "journal", "journal": "Journal of Testing", "volume": 10, "issue": 1, "paper_count": 3}
    ]
    venue = "Conference XYZ"
    expected_output = {
        "Conference XYZ": {
            "2021": [
                {
                    "kind": "proceedings",
                    "part": "Part A",
                    "display_name": "Proceedings of Part A",
                    "paper_count": 5,
                },
                {
                    "kind": "journal",
                    "journal": "Journal of Testing",
                    "display_name": "Journal of Testing volume 10 issue 1",
                    "volume": 10,
                    "issue": 1,
                    "paper_count": 3,
                }
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_missing_required_fields():
    inventory = [
        {"year": 2021, "kind": "proceedings", "part": "Part A", "paper_count": 5},  # Missing part_title
        {"year": 2021, "kind": "journal", "journal": "Journal of Testing", "volume": 10}  # Missing issue and paper_count
    ]
    venue = "Conference XYZ"
    with pytest.raises(KeyError):
        generate_manifest_template(inventory, venue)

def test_unexpected_kind_value():
    inventory = [
        {"year": 2021, "kind": "unknown", "part": "Part A", "part_title": "Proceedings of Part A", "paper_count": 5}
    ]
    venue = "Conference XYZ"
    expected_output = {
        "Conference XYZ": {
            2021: []
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output