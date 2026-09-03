from target_functions.generate_manifest_template_target import generate_manifest_template
import pytest

def test_empty_inventory():
    inventory = []
    venue = "Conference A"
    expected_output = {"Conference A": {}}
    assert generate_manifest_template(inventory, venue) == expected_output

def test_single_proceedings_record():
    inventory = [{"year": 2023, "kind": "proceedings", "part": "Part A", "part_title": "Title A", "paper_count": 10}]
    venue = "Conference A"
    expected_output = {"Conference A": {2023: [{"kind": "proceedings", "part": "Part A", "display_name": "Title A", "paper_count": 10}]}}
    assert generate_manifest_template(inventory, venue) == expected_output

def test_single_journal_record():
    inventory = [{"year": 2023, "kind": "journal", "journal": "Journal A", "volume": "1", "issue": "1", "paper_count": 5}]
    venue = "Journal Venue"
    expected_output = {"Journal Venue": {2023: [{"kind": "journal", "journal": "Journal A", "display_name": "Journal A volume 1 issue 1", "volume": "1", "issue": "1", "paper_count": 5}]}}
    assert generate_manifest_template(inventory, venue) == expected_output

def test_multiple_records_in_same_year():
    inventory = [
        {"year": 2023, "kind": "proceedings", "part": "Part A", "part_title": "Title A", "paper_count": 10},
        {"year": 2023, "kind": "journal", "journal": "Journal A", "volume": "1", "issue": "1", "paper_count": 5}
    ]
    venue = "Conference A"
    expected_output = {
        "Conference A": {
            2023: [
                {"kind": "proceedings", "part": "Part A", "display_name": "Title A", "paper_count": 10},
                {"kind": "journal", "journal": "Journal A", "display_name": "Journal A volume 1 issue 1", "volume": "1", "issue": "1", "paper_count": 5}
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_different_years():
    inventory = [
        {"year": 2022, "kind": "journal", "journal": "Journal B", "volume": "2", "issue": "1", "paper_count": 3},
        {"year": 2023, "kind": "proceedings", "part": "Part B", "part_title": "Title B", "paper_count": 7}
    ]
    venue = "Conference B"
    expected_output = {
        "Conference B": {
            2022: [{"kind": "journal", "journal": "Journal B", "display_name": "Journal B volume 2 issue 1", "volume": "2", "issue": "1", "paper_count": 3}],
            2023: [{"kind": "proceedings", "part": "Part B", "display_name": "Title B", "paper_count": 7}]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_duplicate_records_in_same_year():
    inventory = [
        {"year": 2023, "kind": "journal", "journal": "Journal C", "volume": "3", "issue": "2", "paper_count": 4},
        {"year": 2023, "kind": "journal", "journal": "Journal C", "volume": "3", "issue": "2", "paper_count": 4}
    ]
    venue = "Journal Venue"
    expected_output = {
        "Journal Venue": {
            2023: [
                {"kind": "journal", "journal": "Journal C", "display_name": "Journal C volume 3 issue 2", "volume": "3", "issue": "2", "paper_count": 4},
                {"kind": "journal", "journal": "Journal C", "display_name": "Journal C volume 3 issue 2", "volume": "3", "issue": "2", "paper_count": 4}
            ]
        }
    }
    assert generate_manifest_template(inventory, venue) == expected_output

def test_handling_missing_required_fields():
    inventory = [{"year": 2023, "kind": "proceedings", "part": "Part C", "paper_count": 8}]
    venue = "Conference C"
    with pytest.raises(KeyError):
        generate_manifest_template(inventory, venue)

def test_invalid_year_format():
    inventory = [{"year": "2023a", "kind": "journal", "journal": "Journal D", "volume": "4", "issue": "3", "paper_count": 6}]
    venue = "Journal Venue"
    with pytest.raises(KeyError):
        generate_manifest_template(inventory, venue)