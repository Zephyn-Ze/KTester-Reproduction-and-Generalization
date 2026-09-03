import pytest

from target_functions.generate_manifest_template_target import generate_manifest_template


def test_groups_proceedings_and_journal_records_by_year():
    inventory = [
        {
            "year": "2024",
            "kind": "proceedings",
            "part": "https://dblp.org/db/conf/example/example2024.html",
            "part_title": "Example 2024",
            "paper_count": 12,
        },
        {
            "year": "2024",
            "kind": "journal_issue",
            "journal": "Example Journal",
            "volume": "8",
            "issue": "2",
            "paper_count": 7,
        },
    ]

    assert generate_manifest_template(inventory, "EXAMPLE") == {
        "EXAMPLE": {
            "2024": [
                {
                    "kind": "proceedings",
                    "part": "https://dblp.org/db/conf/example/example2024.html",
                    "display_name": "Example 2024",
                    "paper_count": 12,
                },
                {
                    "kind": "journal",
                    "journal": "Example Journal",
                    "display_name": "Example Journal volume 8 issue 2",
                    "volume": "8",
                    "issue": "2",
                    "paper_count": 7,
                },
            ]
        }
    }


def test_empty_inventory_keeps_the_venue_key():
    assert generate_manifest_template([], "ASE") == {"ASE": {}}


def test_missing_required_field_raises_key_error():
    with pytest.raises(KeyError):
        generate_manifest_template([{"year": "2024"}], "ASE")
