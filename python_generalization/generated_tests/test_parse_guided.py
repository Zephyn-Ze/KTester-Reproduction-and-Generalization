import pytest
from target_functions.parse_bindings_target import parse_bindings

def test_normal_case_with_complete_data():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}, "title": {"value": "Paper Title 1"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}},
        {"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author C"}, "title": {"value": "Paper Title 2"}}
    ]
    venue = "Conference A"
    year = 2023
    result = parse_bindings(bindings, venue, year)
    expected = [
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
    assert result == expected

def test_missing_title_key():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author B"}, "title": {"value": "Paper Title 2"}}
    ]
    venue = "Conference B"
    year = 2023
    result = parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": "Conference B",
            "title": None,
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        },
        {
            "venue": "Conference B",
            "title": "Paper Title 2",
            "year": 2023,
            "url": "http://example.com/paper2",
            "authors": ["Author B"]
        }
    ]
    assert result == expected

def test_empty_bindings_list():
    bindings = []
    venue = "Conference C"
    year = 2023
    result = parse_bindings(bindings, venue, year)
    expected = []
    assert result == expected

def test_missing_required_keys():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}},
        {"authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author B"}}
    ]
    venue = "Conference D"
    year = 2023
    result = parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": "Conference D",
            "title": None,
            "year": 2023,
            "url": "http://example.com/paper2",
            "authors": ["Author B"]
        }
    ]
    assert result == expected

def test_duplicate_authors_for_same_publication():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author B"}}
    ]
    venue = "Conference E"
    year = 2023
    result = parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": "Conference E",
            "title": None,
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": ["Author A", "Author B"]
        }
    ]
    assert result == expected

def test_non_list_bindings_input():
    bindings = "Not a list"
    venue = "Conference F"
    year = 2023
    with pytest.raises(TypeError):
        parse_bindings(bindings, venue, year)

def test_non_dictionary_item_in_bindings():
    bindings = [
        {"publication": {"value": "http://example.com/paper1"}, "authorName": {"value": "Author A"}},
        "Not a dictionary",
        {"publication": {"value": "http://example.com/paper2"}, "authorName": {"value": "Author B"}}
    ]
    venue = "Conference G"
    year = 2023
    result = parse_bindings(bindings, venue, year)
    expected = [
        {
            "venue": "Conference G",
            "title": None,
            "year": 2023,
            "url": "http://example.com/paper1",
            "authors": ["Author A"]
        },
        {
            "venue": "Conference G",
            "title": None,
            "year": 2023,
            "url": "http://example.com/paper2",
            "authors": ["Author B"]
        }
    ]
    assert result == expected