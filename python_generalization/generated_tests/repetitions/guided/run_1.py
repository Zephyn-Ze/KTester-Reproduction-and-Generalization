import pytest
from target_functions.parse_bindings_target import parse_bindings

def test_empty_bindings():
    result = parse_bindings([], "Conference A", 2023)
    assert result == []

def test_missing_required_keys():
    bindings = [{"publication": {"value": "http://example.com/paper1"}}, {"authorName": {"value": "Author A"}}]
    result = parse_bindings(bindings, "Conference B", 2023)
    assert result == []

def test_single_publication_with_multiple_authors():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}}
    ]
    result = parse_bindings(bindings, "Conference C", 2023)
    expected = [{"venue": "Conference C", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A", "Author B"]}]
    assert result == expected

def test_publication_without_title():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}}
    ]
    result = parse_bindings(bindings, "Conference D", 2023)
    expected = [{"venue": "Conference D", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A", "Author B"]}]
    assert result == expected

def test_duplicate_publications():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}}
    ]
    result = parse_bindings(bindings, "Conference E", 2023)
    expected = [{"venue": "Conference E", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]}]
    assert result == expected

def test_valid_input_with_missing_author_name():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper2"}, "title": {"value": "Paper Title"}, "authorName": {}}
    ]
    result = parse_bindings(bindings, "Conference F", 2023)
    expected = [{"venue": "Conference F", "title": "Paper Title", "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]}]
    assert result == expected

def test_non_list_input_type():
    with pytest.raises(TypeError):
        parse_bindings("not a list", "Conference G", 2023)

def test_multiple_publications_with_same_author():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author A"}}
    ]
    result = parse_bindings(bindings, "Conference H", 2023)
    expected = [
        {"venue": "Conference H", "title": None, "year": 2023, "url": "http://example.com/paper1", "authors": ["Author A"]},
        {"venue": "Conference H", "title": None, "year": 2023, "url": "http://example.com/paper2", "authors": ["Author A"]}
    ]
    assert result == expected