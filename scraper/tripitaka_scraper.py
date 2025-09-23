import requests
from bs4 import BeautifulSoup
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def is_valid_tripitaka_content(sinhala_text: str, pali_text: str, title: str) -> bool:
    """
    Validates if the scraped content contains actual Tripitaka content
    rather than just navigation/footer text.
    
    Returns:
        bool: True if content appears to be valid Tripitaka content, False otherwise
    """
    
    # Common phrases that indicate empty/navigation pages
    empty_page_indicators = [
        "උතුම් වූ ධර්මදානය පිණිස මෙම දෙසුම ඔබේ මිතුරන් අතරේ බෙදාහරින්න",  # Share this sermon
        "Previous Next",
        "© 1999 - 2021 Mahamevnawa Buddhist Monastery",
        "© 1999 - 2025 Mahamevnawa Buddhist Monastery",
        "Contact: info@tripitaka.online"
    ]
    
    # Tripitaka structure indicators (positive signals)
    tripitaka_indicators = [
        "මා හට අසන්නට ලැබුණේ",  # "I heard it this way" - common sutta opening
        "ඒවං මේ සුතං",  # Pali version of "Thus I heard"
        "බුදුරජාණන් වහන්සේ",  # Buddha
        "භාග්‍යවත්",  # Blessed One
        "භික්ෂු",  # Monk
        "සූත්‍රය",  # Sutta
        "නිකාය",  # Nikaya
    ]
    
    # Check if title is just generic "tripitaka.online"
    if title.strip() in ["tripitaka.online", "Untitled", ""]:
        print(f"❌ Invalid title: '{title}'")
        return False
    
    # Check total content length (very short content is likely navigation only)
    total_content = sinhala_text + pali_text
    if len(total_content.strip()) < 500:  # Less than 500 chars is likely not real content
        print(f"❌ Content too short: {len(total_content)} characters")
        return False
    
    # Check for empty page indicators
    content_to_check = sinhala_text + " " + pali_text
    empty_indicators_found = []
    for indicator in empty_page_indicators:
        if indicator in content_to_check:
            empty_indicators_found.append(indicator)
    
    # If we found multiple empty page indicators and no Tripitaka indicators, it's likely empty
    if len(empty_indicators_found) >= 2:
        tripitaka_indicators_found = []
        for indicator in tripitaka_indicators:
            if indicator in content_to_check:
                tripitaka_indicators_found.append(indicator)
        
        if len(tripitaka_indicators_found) == 0:
            print(f"❌ Empty page detected. Found indicators: {empty_indicators_found}")
            return False
    
    # Check content quality - repetitive content suggests navigation/footer duplication
    lines = content_to_check.split()
    if len(lines) > 10:
        # Count unique words vs total words to detect repetition
        unique_words = set(lines)
        repetition_ratio = len(unique_words) / len(lines)
        
        # Only flag as repetitive if content is short AND highly repetitive
        # Long content (like actual suttas) can have lower ratios due to repeated concepts
        if repetition_ratio < 0.3 and len(content_to_check) < 2000:  # Only apply to short content
            print(f"❌ High repetition detected in short content (ratio: {repetition_ratio:.2f})")
            return False
        elif repetition_ratio < 0.03:  # More lenient threshold for extremely repetitive content
            print(f"❌ Extremely high repetition detected (ratio: {repetition_ratio:.2f})")
            return False
    
    # Additional check: Look for positive Tripitaka indicators in longer content
    if len(total_content) > 2000:  # For longer content, require at least one Tripitaka indicator
        tripitaka_indicators_found = []
        for indicator in tripitaka_indicators:
            if indicator in content_to_check:
                tripitaka_indicators_found.append(indicator)
        
        if len(tripitaka_indicators_found) > 0:
            print(f"✅ Valid content detected (found indicators: {tripitaka_indicators_found[:3]})")
            return True
        else:
            print(f"⚠️  Long content but no Tripitaka indicators found - may be valid")
            return True  # Give benefit of doubt to long content
    
    print(f"✅ Valid content detected")
    return True

def scrape_tripitaka_page(url: str):
    # Setup Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Setup Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"Scraping URL: {url}")
        driver.get(url)
        
        # Wait for the Angular app to load and content to appear
        # We'll wait for either content to appear or a reasonable timeout
        wait = WebDriverWait(driver, 20)
        
        # Wait a bit for the page to fully load
        time.sleep(5)
        
        # Get the fully rendered HTML
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        
        print(f"Page loaded, parsing content...")
        
        # Try to find title from various possible locations
        title = "Untitled"
        title_selectors = [
            "h1", "h2", ".title", ".sutta-title", 
            "[class*='title']", "[class*='heading']"
        ]
        
        for selector in title_selectors:
            title_element = soup.select_one(selector)
            if title_element and title_element.get_text(strip=True):
                title = title_element.get_text(strip=True)
                print(f"Found title: {title}")
                break
        
        # If no title found in content, try meta tags
        if title == "Untitled":
            meta_title = soup.find("meta", {"property": "og:title"})
            if meta_title and meta_title.get("content"):
                title = meta_title.get("content").strip()
                print(f"Found title in meta: {title}")
            else:
                page_title = soup.find("title")
                if page_title:
                    title = page_title.get_text(strip=True)
                    print(f"Found title in page title: {title}")
        
        # Try various selectors for Sinhala content
        sinhala_text = ""
        sinhala_selectors = [
            "div[lang='si']", "div[lang='sin']", ".sinhala", 
            ".si-text", "[class*='sinhala']", "[lang='si']",
            "div:contains('සූත්‍ර')", "div:contains('ය')"
        ]
        
        for selector in sinhala_selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    sinhala_text = " ".join([el.get_text(" ", strip=True) for el in elements])
                    if sinhala_text:
                        print(f"Found Sinhala text with selector '{selector}': {len(sinhala_text)} chars")
                        break
            except Exception as e:
                continue
        
        # Try various selectors for Pali content
        pali_text = ""
        pali_selectors = [
            "div[lang='pi']", "div[lang='pali']", ".pali", 
            ".pi-text", "[class*='pali']", "[lang='pi']"
        ]
        
        for selector in pali_selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    pali_text = " ".join([el.get_text(" ", strip=True) for el in elements])
                    if pali_text:
                        print(f"Found Pali text with selector '{selector}': {len(pali_text)} chars")
                        break
            except Exception as e:
                continue
        
        # If no specific language content found, let's examine the page structure
        if not sinhala_text and not pali_text:
            print("No specific language content found, examining page structure...")
            
            # Look for common content containers
            content_selectors = [
                ".content", ".main-content", ".text-content",
                ".sutta-content", ".body", "main", "article",
                "[class*='content']", "[class*='text']"
            ]
            
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(" ", strip=True)
                    if len(text) > 100:  # Reasonable content length
                        print(f"Found content with selector '{selector}': {len(text)} chars")
                        # Try to identify if it's Sinhala or Pali based on script
                        if any(char in text for char in 'අආඇඈඉඊඋඌඍඎඑඒඓඔඕඖ'):
                            sinhala_text = text
                        else:
                            pali_text = text
                        break
                if sinhala_text or pali_text:
                    break
        
        # Validate content quality
        is_valid_content = is_valid_tripitaka_content(sinhala_text, pali_text, title)
        
        # Debug: Print some page structure information
        print(f"Page title: {title}")
        print(f"Sinhala content length: {len(sinhala_text)}")
        print(f"Pali content length: {len(pali_text)}")
        print(f"Content valid: {is_valid_content}")
        
        # Save a debug HTML file to examine the structure
        debug_dir = "output/debug"
        os.makedirs(debug_dir, exist_ok=True)
        with open(f"{debug_dir}/page_source.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved debug HTML to {debug_dir}/page_source.html")
        
        return {
            "url": url,
            "title": title,
            "content": {
                "sinhala": sinhala_text,
                "pali": pali_text
            },
            "is_valid_content": is_valid_content,
            "content_quality": "valid" if is_valid_content else "invalid"
        }
        
    except Exception as e:
        print(f"Error scraping page: {e}")
        return {
            "url": url,
            "title": "Error",
            "content": {
                "sinhala": "",
                "pali": ""
            },
            "error": str(e)
        }
    finally:
        driver.quit()

def save_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
