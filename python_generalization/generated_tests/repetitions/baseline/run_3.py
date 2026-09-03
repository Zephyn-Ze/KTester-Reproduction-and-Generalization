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
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author B"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "authorName": {"value": "Author C"},
            "title": {"value": "Title 2"}
        }
    ]
    venue = "Conference A"
    year = 2023
    expected = [
        {
            "venue": venue,
            "title": "Title 1",
            "year": year,
            "url": "http://example.com/paper1",
            "authors": ["Author A", "Author B"]
        },
        {
            "venue": venue,
            "title": "Title 2",
            "year": year,
            "url": "http://example.com/paper2",
            "authors": ["Author C"]
        }
    ]
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    assert result == expected

def test_parse_bindings_missing_fields():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"}
        },
        {
            "authorName": {"value": "Author B"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "title": {"value": "Title 2"}
        }
    ]
    venue = "Conference B"
    year = 2023
    expected = [
        {
            "venue": venue,
            "title": None,
            "year": year,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        }
    ]
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    assert result == expected

def test_parse_bindings_empty_input():
    bindings = []
    venue = "Conference C"
    year = 2023
    expected = []
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    assert result == expected

def test_parse_bindings_duplicate_authors():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"}
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"}
        }
    ]
    venue = "Conference D"
    year = 2023
    expected = [
        {
            "venue": venue,
            "title": None,
            "year": year,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        }
    ]
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    assert result == expected

def test_parse_bindings_no_publication():
    bindings = [
        {
            "authorName": {"value": "Author A"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "authorName": {"value": "Author B"}
        }
    ]
    venue = "Conference E"
    year = 2023
    expected = [
        {
            "venue": venue,
            "title": None,
            "year": year,
            "url": "http://example.com/paper2",
            "authors": ["Author B"]
        }
    ]
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    assert result == expected