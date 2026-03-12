# File: services/memory_service.py
from modules.memory.vector_store import CitewebMemory

class MemoryService:
    def __init__(self):
        self.memory = CitewebMemory()

    def store_website_data(self, clean_text: str, url: str):
        """Bridges the Scraper output to the Vector Store."""
        return self.memory.save_text(clean_text, url)

    def quick_search(self, query: str):
        """Allows for manual memory testing."""
        return self.memory.search(query)