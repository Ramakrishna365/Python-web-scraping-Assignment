import pytest
from processing.validation import validate_record

def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "name_or_title": "A Book",
        "source_url": "http://example.com",
        "price": 10.5,
        "rating": 4
    }
    assert validate_record(record) == []

def test_invalid_source():
    record = {
        "source": "Unknown",
        "name_or_title": "A Book",
        "source_url": "http://example.com"
    }
    assert "Invalid source: Unknown" in validate_record(record)

def test_missing_title():
    record = {
        "source": "Books to Scrape",
        "name_or_title": "",
        "source_url": "http://example.com"
    }
    assert "name_or_title is empty" in validate_record(record)

def test_invalid_url():
    record = {
        "source": "Books to Scrape",
        "name_or_title": "A Book",
        "source_url": "ftp://example.com"
    }
    assert "Invalid source_url: ftp://example.com" in validate_record(record)

def test_invalid_price():
    record = {
        "source": "Books to Scrape",
        "name_or_title": "A Book",
        "source_url": "http://example.com",
        "price": -5.0
    }
    assert "Invalid price: -5.0" in validate_record(record)

def test_invalid_rating():
    record = {
        "source": "Books to Scrape",
        "name_or_title": "A Book",
        "source_url": "http://example.com",
        "rating": 6
    }
    assert "Invalid rating: 6" in validate_record(record)
