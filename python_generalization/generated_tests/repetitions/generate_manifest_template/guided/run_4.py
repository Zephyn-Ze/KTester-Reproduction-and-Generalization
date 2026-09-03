from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_empty_inventory():
    result = generate_manifest_template([], "Conference")
    assert result == {"Conference": {}}

def test_single_proceedings_record():
    inventory = [{"year": 2023, "kind": "proceedings", "part": "Part A", "part_title": "Title A", "paper_count": 5}]
    result = generate_manifest_template(inventory, "Conference")
    assert result == {"Conference": {2023: [{"kind": "proceedings", "part": "Part A", "display_name": "Title A", "paper_count": 5}]}}
    
def test_single_journal_record():
    inventory = [{"year": 2023, "kind": "journal", "journal": "Journal A", "volume": "1", "issue": "1", "paper_count": 3}]
    result = generate_manifest_template(inventory, "Journal Club")
    assert result == {"Journal Club": {2023: [{"kind": "journal", "journal": "Journal A", "display_name": "Journal A volume 1 issue 1", "volume": "1", "issue": "1", "paper_count": 3}]}}
    
def test_multiple_records_same_year():
    inventory = [
        {"year": 2023, "kind": "proceedings", "part": "Part A", "part_title": "Title A", "paper_count": 5},
        {"year": 2023, "kind": "journal", "journal": "Journal B", "volume": "1", "issue": "1", "paper_count": 2}
    ]
    result = generate_manifest_template(inventory, "Conference")
    assert result == {
        "Conference": {
            2023: [
                {"kind": "proceedings", "part": "Part A", "display_name": "Title A", "paper_count": 5},
                {"kind": "journal", "journal": "Journal B", "display_name": "Journal B volume 1 issue 1", "volume": "1", "issue": "1", "paper_count": 2}
            ]
        }
    }

def test_multiple_proceedings_records():
    inventory = [
        {"year": 2023, "kind": "proceedings", "part": "Part A", "part_title": "Title A", "paper_count": 5},
        {"year": 2023, "kind": "proceedings", "part": "Part B", "part_title": "Title B", "paper_count": 10}
    ]
    result = generate_manifest_template(inventory, "Conference")
    assert result == {
        "Conference": {
            2023: [
                {"kind": "proceedings", "part": "Part A", "display_name": "Title A", "paper_count": 5},
                {"kind": "proceedings", "part": "Part B", "display_name": "Title B", "paper_count": 10}
            ]
        }
    }

def test_different_year_types():
    inventory = [
        {"year": "2023", "kind": "journal", "journal": "Journal A", "volume": "1", "issue": "1", "paper_count": 3},
        {"year": 2024, "kind": "proceedings", "part": "Part A", "part_title": "Title A", "paper_count": 5}
    ]
    result = generate_manifest_template(inventory, "Conference")
    assert result == {
        "Conference": {
            "2023": [
                {"kind": "journal", "journal": "Journal A", "display_name": "Journal A volume 1 issue 1", "volume": "1", "issue": "1", "paper_count": 3}
            ],
            2024: [
                {"kind": "proceedings", "part": "Part A", "display_name": "Title A", "paper_count": 5}
            ]
        }
    }

def test_duplicate_records():
    inventory = [
        {"year": 2023, "kind": "journal", "journal": "Journal A", "volume": "1", "issue": "1", "paper_count": 3},
        {"year": 2023, "kind": "journal", "journal": "Journal A", "volume": "1", "issue": "1", "paper_count": 3}
    ]
    result = generate_manifest_template(inventory, "Journal Club")
    assert result == {
        "Journal Club": {
            2023: [
                {"kind": "journal", "journal": "Journal A", "display_name": "Journal A volume 1 issue 1", "volume": "1", "issue": "1", "paper_count": 3},
                {"kind": "journal", "journal": "Journal A", "display_name": "Journal A volume 1 issue 1", "volume": "1", "issue": "1", "paper_count": 3}
            ]
        }
    }

def test_missing_keys_in_records():
    inventory = [{"year": 2023, "kind": "proceedings", "part": "Part A", "paper_count": 5}]
    with pytest.raises(KeyError):
        generate_manifest_template(inventory, "Conference")

def test_incorrect_data_types():
    inventory = [{"year": 2023, "kind": "journal", "journal": "Journal A", "volume": "1", "issue": "1", "paper_count": "three"}]
    with pytest.raises(TypeError):
        generate_manifest_template(inventory, "Journal Club")

def test_mixed_record_types():
    inventory = [
        {"year": 2023, "kind": "proceedings", "part": "Part A", "part_title": "Title A", "paper_count": 5},
        {"year": 2023, "kind": "journal", "journal": "Journal B", "volume": "1", "issue": "1", "paper_count": 2}
    ]
    result = generate_manifest_template(inventory, "Mixed Venue")
    assert result == {
        "Mixed Venue": {
            2023: [
                {"kind": "proceedings", "part": "Part A", "display_name": "Title A", "paper_count": 5},
                {"kind": "journal", "journal": "Journal B", "display_name": "Journal B volume 1 issue 1", "volume": "1", "issue": "1", "paper_count": 2}
            ]
        }
    }