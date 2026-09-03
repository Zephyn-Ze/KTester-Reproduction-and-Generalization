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
        },
    ]
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
    assert parse_bindings(bindings, "Conference A", 2023) == expected_output

def test_parse_bindings_missing_fields():
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
            "title": {"value": "Paper Title 2"}
        },
    ]
    expected_output = [
        {
            "venue": "Conference A",
            "title": "Paper Title 2",
            "year": 2023,
            "url": "http://example.com/paper2",
            "authors": ["Author B"]
        }
    ]
    assert parse_bindings(bindings, "Conference A", 2023) == expected_output

def test_parse_bindings_edge_case_empty():
    bindings = []
    expected_output = []
    assert parse_bindings(bindings, "Conference A", 2023) == expected_output

def test_parse_bindings_no_authors():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "title": {"value": "Paper Title 1"}
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "title": {"value": "Paper Title 2"}
        },
    ]
    expected_output = [
        {
            "venue": "Conference A",
            "title": "Paper Title 1",
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": []
        },
        {
            "venue": "Conference A",
            "title": "Paper Title 2",
            "year": 2023,
            "url": "http://example.com/paper2",
            "authors": []
        }
    ]
    assert parse_bindings(bindings, "Conference A", 2023) == expected_output

def test_parse_bindings_duplicate_authors():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Paper Title 1"}
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"}
        },
    ]
    expected_output = [
        {
            "venue": "Conference A",
            "title": "Paper Title 1",
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        }
    ]
    assert parse_bindings(bindings, "Conference A", 2023) == expected_output