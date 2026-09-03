import pytest
from target_functions import parse_bindings_target

def test_parse_bindings_normal_case():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title 1"},
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author B"},
        },
        {
            "publication": {"value": "http://example.com/paper2"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title 2"},
        }
    ]
    venue = "Conference X"
    year = 2023
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
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
            "authors": ["Author A"]
        }
    ]
    assert result == expected

def test_parse_bindings_missing_keys():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
        },
        {
            "title": {"value": "Title 2"},
            "authorName": {"value": "Author B"},
        },
        {
            "publication": {"value": "http://example.com/paper3"},
        }
    ]
    venue = "Conference Y"
    year = 2022
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": venue,
            "title": None,
            "year": year,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        }
    ]
    assert result == expected

def test_parse_bindings_no_bindings():
    bindings = []
    venue = "Conference Z"
    year = 2021
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    assert result == []

def test_parse_bindings_duplicate_authors():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
            "title": {"value": "Title 1"},
        },
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": "Author A"},
        }
    ]
    venue = "Conference A"
    year = 2020
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": venue,
            "title": "Title 1",
            "year": year,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        }
    ]
    assert result == expected

def test_parse_bindings_edge_case_empty_author():
    bindings = [
        {
            "publication": {"value": "http://example.com/paper1"},
            "authorName": {"value": ""},
            "title": {"value": "Title 1"},
        }
    ]
    venue = "Conference B"
    year = 2019
    result = parse_bindings_target.parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": venue,
            "title": "Title 1",
            "year": year,
            "url": "http://example.com/paper1",
            "authors": [""]
        }
    ]
    assert result == expected