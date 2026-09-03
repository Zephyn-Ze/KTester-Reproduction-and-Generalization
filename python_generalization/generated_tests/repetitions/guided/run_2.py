import pytest
from target_functions.parse_bindings_target import parse_bindings

def test_empty_bindings():
    result = parse_bindings([], "Conference", 2023)
    assert result == []

def test_missing_required_keys():
    result = parse_bindings([{"title": {"value": "Paper Title"}}], "Journal", 2022)
    assert result == []

def test_single_paper_with_one_author():
    result = parse_bindings([{"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}}], "Conference", 2023)
    assert result == [{"venue": "Conference", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]}]

def test_single_paper_with_multiple_authors():
    result = parse_bindings([
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}}
    ], "Conference", 2023)
    assert result == [{"venue": "Conference", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A", "Author B"]}]

def test_multiple_papers_with_unique_urls():
    result = parse_bindings([
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author B"}}
    ], "Conference", 2023)
    assert result == [
        {"venue": "Conference", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]},
        {"venue": "Conference", "title": None, "year": 2023, "url": "http://example.com/paper2", "authors": ["Author B"]}
    ]

def test_duplicate_authors_for_same_paper():
    result = parse_bindings([
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}}
    ], "Conference", 2023)
    assert result == [{"venue": "Conference", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]}]

def test_handling_missing_title():
    result = parse_bindings([
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}, "title": {}}
    ], "Conference", 2023)
    assert result == [{"venue": "Conference", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A", "Author B"]}]

def test_all_items_invalid():
    result = parse_bindings([{"title": {"value": "Paper Title"}}, {"authorName": {"value": "Author A"}}], "Conference", 2023)
    assert result == []

def test_mixed_valid_and_invalid_items():
    result = parse_bindings([
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"title": {"value": "Invalid Item"}}
    ], "Conference", 2023)
    assert result == [{"venue": "Conference", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]}]

def test_non_unique_urls_with_different_authors():
    result = parse_bindings([
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}}
    ], "Conference", 2023)
    assert result == [{"venue": "Conference", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A", "Author B"]}]