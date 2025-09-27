#!/usr/bin/env python3
"""
Quick test script to verify WebDriver fixes
"""
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.tripitaka_scraper import scrape_tripitaka_page_with_retry

def test_scraper():
    """Test the improved scraper with a single URL"""
    test_url = "https://tripitaka.online/sutta/17"  # First Digha Nikaya sutta
    
    print("🧪 Testing improved WebDriver setup...")
    print(f"📄 Test URL: {test_url}")
    print("=" * 60)
    
    try:
        result = scrape_tripitaka_page_with_retry(test_url)
        
        print("\n✅ SCRAPING RESULT:")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Sinhala content: {len(result.get('content', {}).get('sinhala', ''))} characters")
        print(f"Pali content: {len(result.get('content', {}).get('pali', ''))} characters")
        print(f"Content quality: {result.get('content_quality', 'N/A')}")
        print(f"Valid content: {result.get('is_valid_content', False)}")
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("🎉 Test successful!")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")

if __name__ == "__main__":
    test_scraper()