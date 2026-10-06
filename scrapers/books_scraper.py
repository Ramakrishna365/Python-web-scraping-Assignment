from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import logging
from .base_scraper import BaseScraper

class BooksScraper(BaseScraper):
    def __init__(self):
        super().__init__("BooksScraper")
        self.base_url = "https://books.toscrape.com/"

    def scrape(self):
        records = []
        current_url = self.base_url
        
        while current_url:
            self.logger.info(f"Scraping Books page: {current_url}")
            response = self.fetch_page(current_url)
            if not response:
                break
                
            soup = BeautifulSoup(response.content, "lxml")
            books = soup.select("article.product_pod")
            
            for b in books:
                try:
                    record = self.parse_book(b, response.url)
                    records.append(record)
                except Exception as e:
                    self.logger.warning(f"Failed to parse a book record: {e}")
            
            next_el = soup.select_one("li.next > a")
            if next_el:
                current_url = urljoin(response.url, next_el["href"])
            else:
                current_url = None
                
        return records

    def parse_book(self, element, page_url):
        title_el = element.select_one("h3 > a")
        price_el = element.select_one("p.price_color")
        rating_el = element.select_one("p.star-rating")
        
        title = title_el["title"] if title_el and "title" in title_el.attrs else (title_el.get_text(strip=True) if title_el else "")
        source_url = urljoin(page_url, title_el["href"]) if title_el else ""
        price = price_el.get_text(strip=True) if price_el else ""
        rating_class = rating_el.get("class") if rating_el else []
        rating = rating_class[1] if len(rating_class) > 1 else ""
        
        return {
            "source": "Books to Scrape",
            "source_url": source_url,
            "name_or_title": title,
            "category": None,
            "price": price,
            "rating": rating,
            "author": None,
            "tags": None,
            "description": None,
            "scraped_at": datetime.utcnow().isoformat() + "Z"
        }
