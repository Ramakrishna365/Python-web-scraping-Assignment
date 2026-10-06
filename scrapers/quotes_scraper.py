from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import logging
from .base_scraper import BaseScraper

class QuotesScraper(BaseScraper):
    def __init__(self):
        super().__init__("QuotesScraper")
        self.base_url = "https://quotes.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.base_url
        
        while current_url:
            self.logger.info(f"Scraping Quotes page: {current_url}")
            response = self.fetch_page(current_url)
            if not response:
                break
                
            soup = BeautifulSoup(response.content, "lxml")
            quotes = soup.select("div.quote")
            
            for q in quotes:
                try:
                    record = self.parse_quote(q, response.url)
                    records.append(record)
                except Exception as e:
                    self.logger.warning(f"Failed to parse a quote record: {e}")
            
            next_el = soup.select_one("li.next > a")
            if next_el:
                current_url = urljoin(response.url, next_el["href"])
            else:
                current_url = None
                
        return records

    def parse_quote(self, element, page_url):
        text_el = element.select_one("span.text")
        author_el = element.select_one("small.author")
        author_url_el = element.select_one("a[href^='/author/']")
        tag_els = element.select("a.tag")
        
        text = text_el.get_text(strip=True) if text_el else ""
        author = author_el.get_text(strip=True) if author_el else ""
        source_url = urljoin(page_url, author_url_el["href"]) if author_url_el else page_url
        tags = [t.get_text(strip=True) for t in tag_els] if tag_els else []
        # Normalizing tags by joining with ;
        tags_str = ";".join(tags) if tags else None
        
        return {
            "source": "Quotes to Scrape",
            "source_url": source_url,
            "name_or_title": text,
            "category": None,
            "price": None,
            "rating": None,
            "author": author,
            "tags": tags_str,
            "description": None,
            "scraped_at": datetime.utcnow().isoformat() + "Z"
        }
