import pytest
from target_functions import parse_bindings_target

def test_parse_bindings_normal_case():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title A"}
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author B"},
            "title": {"value": "Title A"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "authorName": {"value": "Author C"},
            "title": {"value": "Title B"}
        }
    ]
    result = parse_bindings_target.parse_bindings(bindings, "Venue A", 2023)
    expected = [
        {
            "venue": "Venue A",
            "title": "Title A",
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": ["Author A", "Author B"]
        },
        {
            "venue": "Venue A",
            "title": "Title B",
            "year": 2023,
            "url": "http://example.com/paper2",
            "authors": ["Author C"]
        }
    ]
    assert result == expected

def test_parse_bindings_missing_keys():
    bindings = [
        {
            "authorName": {"value": "Author A"}
        },
        {
            "publication": {"value": "http://example.com/paper1"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "authorName": {"value": "Author B"},
            "title": {"value": "Title B"}
        }
    ]
    result = parse_bindings_target.parse_bindings(bindings, "Venue B", 2023)
    expected = [
        {
            "venue": "Venue B",
            "title": "Title B",
            "year": 2023,
            "url": "http://example.com/paper2",
            "authors": ["Author B"]
        }
    ]
    assert result == expected

def test_parse_bindings_empty_input():
    bindings = []
    result = parse_bindings_target.parse_bindings(bindings, "Venue C", 2023)
    expected = []
    assert result == expected

def test_parse_bindings_duplicate_authors():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title A"}
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title A"}
        }
    ]
    result = parse_bindings_target.parse_bindings(bindings, "Venue D", 2023)
    expected = [
        {
            "venue": "Venue D",
            "title": "Title A",
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        }
    ]
    assert result == expected

def test_parse_bindings_no_authors():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "title": {"value": "Title A"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "title": {"value": "Title B"}
        }
    ]
    result = parse_bindings_target.parse_bindings(bindings, "Venue E", 2023)
    expected = []
    assert result == expected