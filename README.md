# Web Scraping Assignment

## 1. Project Overview
This project is a multi-source web scraping and ETL pipeline built in Python. It scrapes book data from `https://books.toscrape.com/` and quote data from `https://quotes.toscrape.com/`, normalizes the data into a standard schema, cleans, validates, deduplicates, and saves the output to a CSV file and a JSON summary report.

## 2. Objective
To demonstrate the ability to extract data from multiple websites handling pagination dynamically, process data correctly, gracefully handle failures, and write well-structured, testable Python code.

## 3. Data Sources
- **Books to Scrape**: Books listing, parsing book titles, prices, ratings.
- **Quotes to Scrape**: Quotes listing, parsing text, author, and tags.

## 4. Technologies Used
- Python 3
- `requests` (HTTP client)
- `beautifulsoup4` and `lxml` (HTML parsing)
- `pytest` (Unit testing)

## 5. Python Version
Tested on Python 3.10 - 3.12.

## 6. Project Structure
```
scraping_assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── tests/
│   ├── __init__.py
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraper.log
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

## 7. Installation
```bash
pip install -r requirements.txt
```

## 8. Virtual Environment Setup (Optional)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

## 9. Dependencies
- requests
- beautifulsoup4
- lxml
- pytest

## 10. How to run
```bash
python main.py
```

## 11. How pagination works
Pagination is dynamic. The scrapers do not hard-code page numbers. Instead, they look for `li.next > a` element on the page, construct an absolute URL using `urljoin`, and follow it until the element is not found.

## 12. Common data model
Both sources are mapped into one common dictionary schema:
`source`, `source_url`, `name_or_title`, `category`, `price`, `rating`, `author`, `tags`, `description`, `scraped_at`.

## 13. Books field mapping
- `source`: "Books to Scrape"
- `name_or_title`: Book Title
- `source_url`: URL of the book detail page
- `price`: Numeric price (converted from string)
- `rating`: Integer (1-5, converted from class names like "Three")
- Other fields: `None` or `""` (Empty string) if not present.

## 14. Quotes field mapping
- `source`: "Quotes to Scrape"
- `name_or_title`: Quote text
- `author`: Author Name
- `source_url`: Author URL
- `tags`: Semicolon-separated string of normalized tags
- Other fields: `None` or `""` if not present.

## 15. Cleaning approach
- **Whitespace**: Handled non-breaking spaces, converted repeated spaces to a single space, stripped bounding spaces.
- **Prices**: Strip alphabetic characters and convert to `float`.
- **Ratings**: Map text ("One", "Two") to integers (1-5).
- **Tags**: Lowercase, sort alphabetically, join by `;`.

## 16. Validation approach
Checks whether mandatory fields exist (`name_or_title`, `source_url`), limits (`price >= 0`, `rating` in 1-5), and verifies proper URL prefixes (`http(s)://`). Invalid records are discarded and rejection reasons are tallied.

## 17. Deduplication approach
Uses a cryptographic SHA-256 hash (fingerprint) of a normalized representation of the identifying fields. For Books, we hash `source + normalized_title`. For Quotes, we hash `source + normalized_author + normalized_quote_prefix`. We track seen fingerprints in a `set()`.

## 18. Error handling
Handled exceptions gracefully using standard `try/except` blocks. If a page fails to load, it stops that scraper but continues with the next source. If a record fails to parse, it logs the error and moves to the next record. 

## 19. Retry mechanism
The `BaseScraper` uses `urllib3.util.retry.Retry` with a backoff factor of 1.0. It retries 3 times on status codes 429, 500, 502, 503, and 504.

## 20. Logging
Implemented standard Python logging (`logging`). Events are logged to `logs/scraper.log` and the console, including progress and validation rejections.

## 21. Output files
- `output/final_dataset.csv`: Cleaned, valid, deduplicated data.
- `output/summary_report.json`: Metrics (duration, records scraped, rejected, duplicate counts).
- `logs/scraper.log`: Application logs.

## 22. Testing
Test suite is implemented in `tests/` using `pytest`. No internet required. Deliberately tests different scenarios (valid, missing fields, capitalization changes for dedup).
Run with: `python -m pytest tests/`

## 23. Assumptions
- Prices on Books to Scrape are in the same currency and can be cleaned of prefixes.
- Quotes have no titles; the text is stored as the `name_or_title`.

## 24. Known limitations
- The code uses `requests.Session` without async, so it's a bit slow since we added a 0.5s pause to not overwhelm the server.

## 25. Possible future improvements
- Use `asyncio` and `aiohttp` for concurrent scraping.
- Connect to a database for larger crawls to handle state.

## 26. AI usage summary
AI was used to scaffold the boilerplate, implement the data schema accurately as per requirements, and generate the unit tests based on the project instructions. Reviewed heavily and tested locally to ensure 100% compliance.
