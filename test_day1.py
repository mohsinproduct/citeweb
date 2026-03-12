from modules.scrapers.static_scraper import CitewebScraper

scraper = CitewebScraper()
print("Scanning target...")
data = scraper.scrape("https://pakjournals.com/")

if "error" in data:
    print("Error:", data["error"])
else:
    print(f"Token Waste: {data['waste_score']}%")
    print(f"Clean Size: {data['clean_size']} characters")
    print(f"Extracted Routes: {data['sub_urls']}")
    print("-" * 30)
    print(data['clean_text'][:200] + "...") # Preview the first 200 chars