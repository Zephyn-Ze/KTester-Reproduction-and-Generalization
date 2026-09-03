import pytest
from target_functions import parse_bindings

def test_empty_bindings():
    result = parse_bindings([], "Conference A", 2023)
    assert result == []

def test_missing_keys():
    result = parse_bindings([{"title": {"value": "Paper 1"}}], "Conference A", 2023)
    assert result == []

def test_single_valid_entry_with_title():
    result = parse_bindings([{"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}, "title": {"value": "Paper 1"}}], "Conference A", 2023)
    assert result == [{"venue": "Conference A", "title": "Paper 1", "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]}]

def test_single_valid_entry_without_title():
    result = parse_bindings([{"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author B"}}], "Conference A", 2023)
    assert result == [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com/paper2", "authors": ["Author B"]}]

def test_duplicate_authors_for_same_url():
    result = parse_bindings([{"publication": {"value": "http://example.com/paper3"}, "authorName": {"value": "Author C"}}, {"publication": {"value": "http://example.com/paper3"}, "authorName": {"value": "Author C"}}], "Conference A", 2023)
    assert result == [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com/paper3", "authors": ["Author C"]}]

def test_multiple_authors_for_same_url():
    result = parse_bindings([{"publication": {"value": "http://example.com/paper4"}, "authorName": {"value": "Author D"}}, {"publication": {"value": "http://example.com/paper4"}, "authorName": {"value": "Author E"}}], "Conference A", 2023)
    assert result == [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com/paper4", "authors": ["Author D", "Author E"]}]

def test_different_publications_same_author():
    result = parse_bindings([{"publication": {"value": "http://example.com/paper5"}, "authorName": {"value": "Author F"}}, {"publication": {"value": "http://example.com/paper6"}, "authorName": {"value": "Author F"}}], "Conference A", 2023)
    assert result == [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com/paper5", "authors": ["Author F"]}, {"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com/paper6", "authors": ["Author F"]}]

def test_mixed_valid_and_invalid_entries():
    result = parse_bindings([{"publication": {"value": "http://example.com/paper7"}, "authorName": {"value": "Author G"}}, {"title": {"value": "Invalid Entry"}}, {"publication": {"value": "http://example.com/paper8"}, "authorName": {"value": "Author H"}}], "Conference A", 2023)
    assert result == [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com/paper7", "authors": ["Author G"]}, {"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com/paper8", "authors": ["Author H"]}]

def test_non_list_input():
    with pytest.raises(TypeError):
        parse_bindings("this is not a list", "Conference A", 2023)

def test_invalid_year_type():
    result = parse_bindings([{"publication": {"value": "http://example.com/paper9"}, "authorName": {"value": "Author I"}}], "Conference A", "not an integer")
    assert result == [{"venue": "Conference A", "title": None, "year": "not an integer", "url": "http://example.com/paper9", "authors": ["Author I"]}]