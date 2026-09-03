import pytest
from target_functions.parse_bindings_target import parse_bindings

def test_empty_bindings():
    result = parse_bindings([], "Conference A", 2023)
    assert result == []

def test_missing_keys():
    bindings = [{"publication": {"value": "http://example.com/paper1"}}, {"authorName": {"value": "Author A"}}]
    result = parse_bindings(bindings, "Conference B", 2023)
    assert result == []

def test_valid_bindings_with_title():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}, "title": {"value": "Title A"}},
        {"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author B"}}
    ]
    result = parse_bindings(bindings, "Conference C", 2023)
    expected = [
        {"venue": "Conference C", "title": "Title A", "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]},
        {"venue": "Conference C", "title": None, "year": 2023, "url": "http://example.com/paper2", "authors": ["Author B"]}
    ]
    assert result == expected

def test_duplicate_authors():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}}
    ]
    result = parse_bindings(bindings, "Conference D", 2023)
    expected = [
        {"venue": "Conference D", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A", "Author B"]}
    ]
    assert result == expected

def test_different_authors_for_same_publication():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}}
    ]
    result = parse_bindings(bindings, "Conference E", 2023)
    expected = [
        {"venue": "Conference E", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A", "Author B"]}
    ]
    assert result == expected

def test_missing_title_handling():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author B"}, "title": {"value": "Title B"}}
    ]
    result = parse_bindings(bindings, "Conference F", 2023)
    expected = [
        {"venue": "Conference F", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]},
        {"venue": "Conference F", "title": "Title B", "year": 2023, "url": "http://example.com/paper2", "authors": ["Author B"]}
    ]
    assert result == expected

def test_invalid_data_types():
    with pytest.raises(TypeError):
        parse_bindings("invalid_string", "Conference G", 2023)

def test_incorrectly_structured_dictionaries():
    bindings = [{"publication": "http://example.com/paper1", "authorName": {"value": "Author A"}}]
    result = parse_bindings(bindings, "Conference H", 2023)
    assert result == []