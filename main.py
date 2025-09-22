
---

### `scraper/tripitaka_scraper.py`
```python
import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_tripitaka_page(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Title
    title_element = soup.find("h1") or soup.find("h2")
    title = title_element.get_text(strip=True) if title_element else "Untitled"

    # Sinhala
    sinhala_div = soup.find("div", {"lang": "si"})
    sinhala_text = sinhala_div.get_text(" ", strip=True) if sinhala_div else ""

    # Pali
    pali_div = soup.find("div", {"lang": "pi"})
    pali_text = pali_div.get_text(" ", strip=True) if pali_div else ""

    return {
        "url": url,
        "title": title,
        "content": {
            "sinhala": sinhala_text,
            "pali": pali_text
        }
    }

def save_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
