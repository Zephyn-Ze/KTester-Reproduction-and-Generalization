import pytest
from target_functions import parse_bindings_target

def test_parse_bindings_normal_case():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Paper Title 1"}
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author B"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "authorName": {"value": "Author C"},
            "title": {"value": "Paper Title 2"}
        }
    ]
    venue = "Conference A"
    year = 2023
    expected_output = [
        {
            "venue": "Conference A",
            "title": "Paper Title 1",
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": ["Author A", "Author B"]
        },
        {
            "venue": "Conference A",
            "title": "Paper Title 2",
            "year": 2023,
            "url": "http://example.com/paper2",
            "authors": ["Author C"]
        }
    ]
    assert parse_bindings_target.parse_bindings(bindings, venue, year) == expected_output

def test_parse_bindings_missing_keys():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "title": {"value": "Paper Title 1"}
        },
        {
            "authorName": {"value": "Author A"}
        }
    ]
    venue = "Conference B"
    year = 2023
    expected_output = []
    assert parse_bindings_target.parse_bindings(bindings, venue, year) == expected_output

def test_parse_bindings_empty_input():
    bindings = []
    venue = "Conference C"
    year = 2023
    expected_output = []
    assert parse_bindings_target.parse_bindings(bindings, venue, year) == expected_output

def test_parse_bindings_edge_case_duplicate_authors():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Paper Title 1"}
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"}
        }
    ]
    venue = "Conference D"
    year = 2023
    expected_output = [
        {
            "venue": "Conference D",
            "title": "Paper Title 1",
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        }
    ]
    assert parse_bindings_target.parse_bindings(bindings, venue, year) == expected_output

def test_parse_bindings_edge_case_no_publication():
    bindings = [
        {
            "authorName": {"value": "Author A"},
            "title": {"value": "Paper Title 1"}
        }
    ]
    venue = "Conference E"
    year = 2023
    expected_output = []
    assert parse_bindings_target.parse_bindings(bindings, venue, year) == expected_output