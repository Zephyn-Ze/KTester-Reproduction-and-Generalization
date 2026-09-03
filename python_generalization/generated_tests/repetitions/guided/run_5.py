import pytest
from target_functions import parse_bindings_target

def test_empty_bindings():
    result = parse_bindings_target.parse_bindings([], "Conference A", 2023)
    assert result == []

def test_missing_required_keys():
    result = parse_bindings_target.parse_bindings([{"authorName": {"value": "Alice"}}, {"publication": {"value": "http://example.com"}}], "Conference A", 2023)
    assert result == []

def test_single_publication_with_one_author():
    result = parse_bindings_target.parse_bindings([{"publication": {"value": "http://example.com"}, "authorName": {"value": "Alice"}}], "Conference A", 2023)
    expected = [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com", "authors": ["Alice"]}]
    assert result == expected

def test_single_publication_with_multiple_authors():
    result = parse_bindings_target.parse_bindings([
        {"publication": {"value": "http://example.com"}, "authorName": {"value": "Alice"}},
        {"publication": {"value": "http://example.com"}, "authorName": {"value": "Bob"}}
    ], "Conference A", 2023)
    expected = [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com", "authors": ["Alice", "Bob"]}]
    assert result == expected

def test_multiple_publications_with_unique_urls():
    result = parse_bindings_target.parse_bindings([
        {"publication": {"value": "http://example1.com"}, "authorName": {"value": "Alice"}},
        {"publication": {"value": "http://example2.com"}, "authorName": {"value": "Bob"}}
    ], "Conference A", 2023)
    expected = [
        {"venue": "Conference A", "title": None, "year": 2023, "url": "http://example1.com", "authors": ["Alice"]},
        {"venue": "Conference A", "title": None, "year": 2023, "url": "http://example2.com", "authors": ["Bob"]}
    ]
    assert result == expected

def test_duplicate_authors_for_same_publication():
    result = parse_bindings_target.parse_bindings([
        {"publication": {"value": "http://example.com"}, "authorName": {"value": "Alice"}},
        {"publication": {"value": "http://example.com"}, "authorName": {"value": "Alice"}}
    ], "Conference A", 2023)
    expected = [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com", "authors": ["Alice"]}]
    assert result == expected

def test_title_is_missing():
    result = parse_bindings_target.parse_bindings([{"publication": {"value": "http://example.com"}, "authorName": {"value": "Alice"}, "title": {}}], "Conference A", 2023)
    expected = [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com", "authors": ["Alice"]}]
    assert result == expected

def test_non_list_bindings_input():
    with pytest.raises(TypeError):
        parse_bindings_target.parse_bindings("not a list", "Conference A", 2023)

def test_invalid_year_type():
    result = parse_bindings_target.parse_bindings([{"publication": {"value": "http://example.com"}, "authorName": {"value": "Alice"}}], "Conference A", "2023")
    expected = [{"venue": "Conference A", "title": None, "year": "2023", "url": "http://example.com", "authors": ["Alice"]}]
    assert result == expected

def test_mixed_valid_and_invalid_bindings():
    result = parse_bindings_target.parse_bindings([
        {"publication": {"value": "http://example.com"}, "authorName": {"value": "Alice"}},
        {"publication": {"value": "http://example.com"}, "authorName": {"value": "Bob"}},
        {"wrongKey": {"value": "http://example.com"}}
    ], "Conference A", 2023)
    expected = [{"venue": "Conference A", "title": None, "year": 2023, "url": "http://example.com", "authors": ["Alice", "Bob"]}]
    assert result == expected