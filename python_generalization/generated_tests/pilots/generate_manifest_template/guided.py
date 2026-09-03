from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_empty_inventory():
    result = generate_manifest_template([], "Conference 2023")
    assert result == {"Conference 2023": {}}

def test_single_proceedings_record():
    inventory = [{"year": 2023, "kind": "proceedings", "part": "Part A", "part_title": "Introduction to Testing", "paper_count": 5}]
    result = generate_manifest_template(inventory, "Conference 2023")
    expected = {"Conference 2023": {2023: [{"kind": "proceedings", "part": "Part A", "display_name": "Introduction to Testing", "paper_count": 5}]}}
    assert result == expected

def test_single_journal_record():
    inventory = [{"year": 2023, "kind": "journal", "journal": "Journal of Testing", "volume": 1, "issue": 1, "paper_count": 3}]
    result = generate_manifest_template(inventory, "Conference 2023")
    expected = {"Conference 2023": {2023: [{"kind": "journal", "journal": "Journal of Testing", "display_name": "Journal of Testing volume 1 issue 1", "volume": 1, "issue": 1, "paper_count": 3}]}}
    assert result == expected

def test_multiple_records_same_year():
    inventory = [
        {"year": 2023, "kind": "proceedings", "part": "Part A", "part_title": "Introduction", "paper_count": 5},
        {"year": 2023, "kind": "journal", "journal": "Journal A", "volume": 1, "issue": 1, "paper_count": 2}
    ]
    result = generate_manifest_template(inventory, "Conference 2023")
    expected = {
        "Conference 2023": {
            2023: [
                {"kind": "proceedings", "part": "Part A", "display_name": "Introduction", "paper_count": 5},
                {"kind": "journal", "journal": "Journal A", "display_name": "Journal A volume 1 issue 1", "volume": 1, "issue": 1, "paper_count": 2}
            ]
        }
    }
    assert result == expected

def test_multiple_years_in_inventory():
    inventory = [
        {"year": 2022, "kind": "journal", "journal": "Journal B", "volume": 2, "issue": 1, "paper_count": 4},
        {"year": 2023, "kind": "proceedings", "part": "Part B", "part_title": "Advanced Testing", "paper_count": 6}
    ]
    result = generate_manifest_template(inventory, "Conference 2023")
    expected = {
        "Conference 2023": {
            2022: [
                {"kind": "journal", "journal": "Journal B", "display_name": "Journal B volume 2 issue 1", "volume": 2, "issue": 1, "paper_count": 4}
            ],
            2023: [
                {"kind": "proceedings", "part": "Part B", "display_name": "Advanced Testing", "paper_count": 6}
            ]
        }
    }
    assert result == expected

def test_duplicate_records_same_year():
    inventory = [
        {"year": 2023, "kind": "journal", "journal": "Journal C", "volume": 3, "issue": 2, "paper_count": 1},
        {"year": 2023, "kind": "journal", "journal": "Journal C", "volume": 3, "issue": 2, "paper_count": 1}
    ]
    result = generate_manifest_template(inventory, "Conference 2023")
    expected = {
        "Conference 2023": {
            2023: [
                {"kind": "journal", "journal": "Journal C", "display_name": "Journal C volume 3 issue 2", "volume": 3, "issue": 2, "paper_count": 1},
                {"kind": "journal", "journal": "Journal C", "display_name": "Journal C volume 3 issue 2", "volume": 3, "issue": 2, "paper_count": 1}
            ]
        }
    }
    assert result == expected

def test_non_standard_year_type():
    inventory = [{"year": "2023", "kind": "journal", "journal": "Journal D", "volume": 4, "issue": 3, "paper_count": 5}]
    result = generate_manifest_template(inventory, "Conference 2023")
    expected = {
        "Conference 2023": {
            "2023": [
                {"kind": "journal", "journal": "Journal D", "display_name": "Journal D volume 4 issue 3", "volume": 4, "issue": 3, "paper_count": 5}
            ]
        }
    }
    assert result == expected

def test_missing_required_fields():
    inventory = [{"year": 2023, "kind": "proceedings", "part": "Part C", "paper_count": 2}]
    with pytest.raises(KeyError):
        generate_manifest_template(inventory, "Conference 2023")

def test_invalid_inventory_type():
    inventory = None
    with pytest.raises(TypeError):
        generate_manifest_template(inventory, "Conference 2023")

def test_mixed_record_types():
    inventory = [
        {"year": 2023, "kind": "proceedings", "part": "Part D", "part_title": "Final Thoughts", "paper_count": 1},
        {"year": 2023, "kind": "journal", "journal": "Journal E", "volume": 5, "issue": 4, "paper_count": 10}
    ]
    result = generate_manifest_template(inventory, "Conference 2023")
    expected = {
        "Conference 2023": {
            2023: [
                {"kind": "proceedings", "part": "Part D", "display_name": "Final Thoughts", "paper_count": 1},
                {"kind": "journal", "journal": "Journal E", "display_name": "Journal E volume 5 issue 4", "volume": 5, "issue": 4, "paper_count": 10}
            ]
        }
    }
    assert result == expected