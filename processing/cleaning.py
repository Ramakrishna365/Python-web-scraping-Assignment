import re

def clean_text(text: str) -> str:
    """Removes unnecessary whitespace and normalizes text."""
    if not text:
        return ""
    # Replace non-breaking spaces and tabs with normal space
    text = text.replace('\xa0', ' ').replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def strip_quotes(text: str) -> str:
    """Removes leading/trailing quotation marks if present."""
    if not text:
        return ""
    if text.startswith('“') and text.endswith('”'):
        text = text[1:-1]
    elif text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text.strip()

def clean_price(price_str: str) -> float | None:
    """Converts price string to float, e.g. '£51.77' -> 51.77."""
    if not price_str:
        return None
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned)
    except ValueError:
        return None

def clean_rating(rating_str: str) -> int | None:
    """Converts textual ratings (One, Two, etc.) to integers."""
    if not rating_str:
        return None
    mapping = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5
    }
    cleaned = rating_str.strip().lower()
    return mapping.get(cleaned, None)

def clean_tags(tags_str: str) -> str | None:
    """Normalizes tags: lowercase, trim, sort, join by ;."""
    if not tags_str:
        return None
    tags = tags_str.split(';')
    cleaned_tags = [clean_text(t).lower() for t in tags if t.strip()]
    cleaned_tags.sort()
    return ";".join(cleaned_tags) if cleaned_tags else None

def normalize_url(url: str) -> str:
    """Basic normalization for URL."""
    if not url:
        return ""
    return url.strip()

def clean_record(record: dict) -> dict:
    """Applies cleaning to a single record."""
    cleaned = record.copy()
    
    cleaned['name_or_title'] = clean_text(record.get('name_or_title', ''))
    if cleaned['source'] == 'Quotes to Scrape':
        cleaned['name_or_title'] = strip_quotes(cleaned['name_or_title'])
        
    cleaned['source_url'] = normalize_url(record.get('source_url', ''))
    
    if cleaned['price']:
        cleaned['price'] = clean_price(record.get('price'))
        
    if cleaned['rating']:
        cleaned['rating'] = clean_rating(record.get('rating'))
        
    if cleaned['author']:
        cleaned['author'] = clean_text(record.get('author'))
        
    if cleaned['tags']:
        cleaned['tags'] = clean_tags(record.get('tags'))
        
    return cleaned
