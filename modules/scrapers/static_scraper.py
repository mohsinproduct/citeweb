# File: modules/scrapers/static_scraper.py
import requests
from bs4 import BeautifulSoup
from modules.scrapers.base import BaseScraper
import urllib3
from urllib.parse import urljoin, urlparse

# Security Bypass: Academic and legacy sites often have misconfigured SSL certs.
# We suppress the warning to ensure uninterrupted automated auditing.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CitewebScraper(BaseScraper):
    def __init__(self):
        # We spoof our identity to prevent basic bot-blocking firewalls from dropping our requests.
        self.headers = {'User-Agent': 'citeweb-auditor/1.0'}

    def calculate_waste(self, raw: int, clean: int) -> float:
        """Calculates Token Waste: The percentage of characters that are NOT human-readable text."""
        if raw == 0: return 0.0
        return round((1 - (clean / raw)) * 100, 2)

    def extract_nav_links(self, soup: BeautifulSoup, base_url: str, limit: int = 3) -> list:
        """
        Heuristic Routing: Modern sites hide navigation outside of standard <nav> tags. 
        This dynamically maps sub-pages to simulate how an AI spider would traverse the site.
        """
        nav_links = set()
        domain = urlparse(base_url).netloc
        normalized_base = base_url.rstrip('/')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Filter out Javascript triggers and email links
            if not href or href.startswith(('javascript:', 'mailto:', 'tel:')):
                continue
                
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            
            # Constraint: Stay within the target domain and avoid infinite scroll anchors
            if parsed_url.netloc == domain:
                clean_url = full_url.split('#')[0].rstrip('/')
                
                if clean_url != normalized_base and clean_url not in nav_links:
                    nav_links.add(clean_url)
                    
            # Hardware Constraint: Limit RAM usage by strictly capping route extraction
            if len(nav_links) >= limit:
                break
                
        return list(nav_links)

    def scrape(self, url: str) -> dict:
        try:
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
            
            raw_content = response.text 
            soup = BeautifulSoup(raw_content, 'html.parser') 
            
            # --- NEW: Structural Audit Logic ---
            audit_log = []
            
            # Define what we hate (Noise) vs. what we love (Signal)
            noise_tags = ['script', 'style', 'nav', 'footer', 'header', 'aside']
            signal_tags = ['h1', 'h2', 'h3', 'p', 'li']

            # Track the 'Noise' we are removing
            for tag in noise_tags:
                found = soup.find_all(tag)
                if found:
                    audit_log.append({"tag": f"<{tag}>", "action": "❌ Removed", "reason": "Non-semantic Clutter"})
                    for el in found: el.decompose()

            # Track the 'Signal' we are keeping
            content_tags = soup.find_all(signal_tags)
            for tag_name in signal_tags:
                if soup.find_all(tag_name):
                    audit_log.append({"tag": f"<{tag_name}>", "action": "✅ Preserved", "reason": "High Citation Value"})

            # ... (rest of the existing scraping logic)

            clean_text = "\n".join([t.get_text().strip() for t in content_tags if len(t.get_text()) > 20])

            return {
                "url": url,
                "clean_text": clean_text,
                "raw_size": len(raw_content),
                "clean_size": len(clean_text),
                "waste_score": self.calculate_waste(len(raw_content), len(clean_text)),
                "sub_urls": self.extract_nav_links(soup, url, limit=3),
                "audit_log": audit_log # <--- PASS THIS TO THE UI
            }
        except Exception as e:
            return {"error": str(e)}