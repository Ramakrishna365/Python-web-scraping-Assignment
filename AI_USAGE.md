# AI Usage

## Tool
Antigravity 

## Usage
- Project structure planning and boilerplate creation.
- Scraper implementation assistance (handling BS4 selectors for nested HTML elements).
- Deduplication and Validation logic implementation.
- Pytest test generation (simulating different edge cases for string validation and hashing).
- Documenting the pipeline inside README.md.

## Review
All generated code was manually reviewed. 
I reviewed the BaseScraper retry configuration to ensure exponential backoff was implemented.
I inspected the cleaning routines for prices to ensure we drop characters correctly instead of doing simple string replacement.

## Verification
- `pytest` executed properly and all tests passed.
- `python main.py` was fully run locally.
- Output CSV (`output/final_dataset.csv`) and JSON report (`output/summary_report.json`) were checked to ensure numbers reconcile completely.
- Logs (`logs/scraper.log`) show paginations works dynamically without hitting any hard-coded limits.
