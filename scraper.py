import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_books(url):
    print(f"🔍 Scraping: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    business_containers = soup.find_all("article")
    
    print(f"📦 Found {len(business_containers)} articles")
    
    data = []

    for biz in business_containers:
        try:
            name_tag = biz.find("h3")
            name = name_tag.text.strip() if name_tag else "N/A"
            
            price_tag = biz.find("p", class_="price_color")
            price = price_tag.text.strip() if price_tag else "N/A"
            
            if name != "N/A":
                data.append({
                    "Book Name": name,
                    "Price": price
                })
        except:
            continue

    return data

def save_to_csv(data, filename="business_data.csv"):
    if not data:
        print("❌ No data to save.")
        return
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"✅ Saved {len(data)} books to {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ ERROR: You forgot the URL!")
        print("💡 Usage: python scraper.py 'http://books.toscrape.com/'")
        sys.exit(1)
    
    target_url = sys.argv[1]
    scraped_data = scrape_books(target_url)
    save_to_csv(scraped_data)