# File: modules/scrapers/base.py
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """
    Abstract blueprint for all ingestion engines. 
    Enforces the return of standardized metric dictionaries to the Service Layer.
    """
    
    @abstractmethod
    def scrape(self, url: str) -> dict:
        """
        Must extract clean text and calculate spatial metadata (raw vs. clean size).
        """
        pass

    @abstractmethod
    def calculate_waste(self, raw: int, clean: int) -> float:
        """
        Must mathematically define the ratio of digital noise to semantic signal.
        """
        pass