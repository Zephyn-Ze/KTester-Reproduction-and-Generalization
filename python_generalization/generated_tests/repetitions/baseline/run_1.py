import pytest
from target_functions import parse_bindings_target

def test_parse_bindings_normal_case():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title 1"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "authorName": {"value": "Author B"},
            "title": {"value": "Title 2"}
        }
    ]
    venue = "Conference"
    year = 2023
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": venue,
            "title": "Title 1",
            "year": year,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        },
        {
            "venue": venue,
            "title": "Title 2",
            "year": year,
            "url": "http://example.com/paper2",
            "authors": ["Author B"]
        }
    ]
    assert result == expected

def test_parse_bindings_duplicate_authors():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title 1"}
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title 1"}
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author B"},
            "title": {"value": "Title 1"}
        }
    ]
    venue = "Conference"
    year = 2023
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": venue,
            "title": "Title 1",
            "year": year,
            "url": "http://example.com/paper1",
            "authors": ["Author A", "Author B"]
        }
    ]
    assert result == expected

def test_parse_bindings_missing_fields():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "title": {"value": "Title 1"}
        },
        {
            "authorName": {"value": "Author B"},
            "title": {"value": "Title 2"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "authorName": {"value": "Author C"}
        }
    ]
    venue = "Conference"
    year = 2023
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": venue,
            "title": None,
            "year": year,
            "url": "http://example.com/paper2",
            "authors": ["Author C"]
        }
    ]
    assert result == expected

def test_parse_bindings_empty_input():
    bindings = []
    venue = "Conference"
    year = 2023
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    expected = []
    assert result == expected

def test_parse_bindings_no_publication_or_author():
    bindings = [
        {
            "title": {"value": "Title 1"}
        },
        {
            "publication": {"value": "http://example.com/paper2"}
        }
    ]
    venue = "Conference"
    year = 2023
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    expected = []
    assert result == expected