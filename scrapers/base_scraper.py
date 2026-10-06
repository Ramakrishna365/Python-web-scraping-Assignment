import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import logging

class BaseScraper:
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
        self.session = requests.Session()
        
        # Configure retries
        retry = Retry(
            total=3,
            backoff_factor=1.0,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        })
        
    def fetch_page(self, url: str, timeout: int = 10):
        """Fetch a page with standard error handling and rate limiting."""
        time.sleep(0.5)  # Rate limiting
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            return None
