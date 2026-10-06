import pytest
from processing.cleaning import clean_text, strip_quotes, clean_price, clean_rating, clean_tags, normalize_url

def test_clean_text():
    assert clean_text("  hello   world  \t \n ") == "hello world"
    assert clean_text("Some\xa0Text") == "Some Text"
    assert clean_text(None) == ""

def test_strip_quotes():
    assert strip_quotes('"Hello"') == "Hello"
    assert strip_quotes("“Hello”") == "Hello"
    assert strip_quotes("Hello") == "Hello"

def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("10.0") == 10.0
    assert clean_price(None) is None
    assert clean_price("abc") is None

def test_clean_rating():
    assert clean_rating("One") == 1
    assert clean_rating("  three  ") == 3
    assert clean_rating("Five") == 5
    assert clean_rating("invalid") is None

def test_clean_tags():
    assert clean_tags(" Zzz ; aaa ; bbb ") == "aaa;bbb;zzz"
    assert clean_tags("") is None
    
def test_normalize_url():
    assert normalize_url(" http://example.com ") == "http://example.com"
