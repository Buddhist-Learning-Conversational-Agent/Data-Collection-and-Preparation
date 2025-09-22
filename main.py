from scraper.tripitaka_scraper import scrape_tripitaka_page, save_json

if __name__ == "__main__":
    url = "https://tripitaka.online/sutta/17"
    data = scrape_tripitaka_page(url)
    save_json(data, "output/samples/sutta_17.json")
    print("✅ Scraped and saved sutta_17.json")
