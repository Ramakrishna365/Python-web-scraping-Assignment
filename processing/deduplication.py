import re
import hashlib

def normalize_for_fingerprint(text: str) -> str:
    """Normalizes text for fingerprint generation: lowercase, strip whitespace, remove punctuation."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_fingerprint(record: dict) -> str:
    """Generates a deterministic fingerprint for a record."""
    source = record.get("source", "")
    if source == "Books to Scrape":
        title = normalize_for_fingerprint(record.get("name_or_title", ""))
        identity = f"{source}|{title}"
    elif source == "Quotes to Scrape":
        author = normalize_for_fingerprint(record.get("author", ""))
        quote_text = normalize_for_fingerprint(record.get("name_or_title", ""))[:50]
        identity = f"{source}|{author}|{quote_text}"
    else:
        identity = f"unknown|{record.get('name_or_title', '')}"
        
    return hashlib.sha256(identity.encode('utf-8')).hexdigest()

def deduplicate(records: list[dict]) -> tuple[list[dict], int]:
    """
    Removes duplicates based on fingerprints.
    Returns (unique_records, duplicate_count)
    """
    seen_fingerprints = set()
    unique_records = []
    duplicate_count = 0
    
    for record in records:
        fingerprint = generate_fingerprint(record)
        if fingerprint in seen_fingerprints:
            duplicate_count += 1
        else:
            seen_fingerprints.add(fingerprint)
            unique_records.append(record)
            
    return unique_records, duplicate_count
