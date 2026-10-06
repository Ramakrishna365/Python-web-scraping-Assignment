import pytest
from processing.deduplication import deduplicate, generate_fingerprint

def test_deduplicate_books():
    r1 = {"source": "Books to Scrape", "name_or_title": "Example Book Title"}
    r2 = {"source": "Books to Scrape", "name_or_title": " Example Book Title "}
    r3 = {"source": "Books to Scrape", "name_or_title": "EXAMPLE BOOK TITLE"}
    
    unique, count = deduplicate([r1, r2, r3])
    assert len(unique) == 1
    assert count == 2

def test_deduplicate_quotes():
    r1 = {"source": "Quotes to Scrape", "author": "Albert Einstein", "name_or_title": "A person who never made a mistake never tried anything new."}
    r2 = {"source": "Quotes to Scrape", "author": "albert einstein", "name_or_title": "A PERSON who never made a mistake never tried anything new.!!"}
    
    unique, count = deduplicate([r1, r2])
    assert len(unique) == 1
    assert count == 1
