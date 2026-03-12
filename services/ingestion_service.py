# File: services/ingestion_service.py
from modules.scrapers.static_scraper import CitewebScraper

class IngestionService:
    """
    The orchestration layer. It manages the Scraper worker so the 
    Streamlit UI doesn't have to handle the complex backend logic.
    """
    def __init__(self):
        self.scraper = CitewebScraper()

    def process_url(self, url: str) -> dict:
        """Executes the ingestion pipeline."""
        return self.scraper.scrape(url)