def validate_record(record: dict) -> list[str]:
    """
    Validates a record and returns a list of problems.
    If the list is empty, the record is valid.
    """
    problems = []
    
    # 1. source is one of "Books to Scrape", "Quotes to Scrape"
    if record.get("source") not in ["Books to Scrape", "Quotes to Scrape"]:
        problems.append(f"Invalid source: {record.get('source')}")
        
    # 2. name_or_title is not empty
    if not record.get("name_or_title"):
        problems.append("name_or_title is empty")
        
    # 3. source_url starts with http:// or https://
    url = record.get("source_url", "")
    if not (url.startswith("http://") or url.startswith("https://")):
        problems.append(f"Invalid source_url: {url}")
        
    # 4. price, when present, is numeric and >= 0
    price = record.get("price")
    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            problems.append(f"Invalid price: {price}")
            
    # 5. rating, when present, is an integer from 1 to 5
    rating = record.get("rating")
    if rating is not None:
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            problems.append(f"Invalid rating: {rating}")
            
    return problems
