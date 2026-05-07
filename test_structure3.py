import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - Category Pages")
print("=" * 60)

# Test category pages
for cat in ["series", "movie", "popular", "latest"]:
    url = f"https://piratexplay.cc/category/{cat}"
    print(f"\n[{cat}] {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        print(f"  Status: {r.status_code}, Length: {len(r.text)}")
        
        # Look for content items
        # Try different selectors
        items = soup.select(".item") or soup.select(".post") or soup.select("article") or soup.select(".card")
        print(f"  Items found: {len(items)}")
        
        # Look for links with series/movie in href
        links = soup.find_all("a", href=True)
        content_links = [l for l in links if "/series/" in l.get("href", "") or "/movie/" in l.get("href", "")]
        print(f"  Content links: {len(content_links)}")
        for link in content_links[:5]:
            href = link.get("href", "")
            text = link.get_text(strip=True)
            if text:
                print(f"    [{text[:50]}] -> {href}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("PirateXPlay.cc - Search Test")
print("=" * 60)

for query in ["doraemon", "naruto", "one piece"]:
    url = f"https://piratexplay.cc/?s={query}"
    print(f"\nSearch: {query}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        print(f"  Status: {r.status_code}, Length: {len(r.text)}")
        
        links = soup.find_all("a", href=True)
        content_links = [l for l in links if "/series/" in l.get("href", "") or "/movie/" in l.get("href", "")]
        print(f"  Content links: {len(content_links)}")
        for link in content_links[:5]:
            href = link.get("href", "")
            text = link.get_text(strip=True)
            if text:
                print(f"    [{text[:50]}] -> {href}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("PirateXPlay.cc - Series Page Details")
print("=" * 60)

# Get a series page
r = requests.get("https://piratexplay.cc/category/series", headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")
links = soup.find_all("a", href=True)
series_links = [l for l in links if "/series/" in l.get("href", "")]

if series_links:
    first_series = series_links[0].get("href", "")
    print(f"\nTesting series: {first_series}")
    r = requests.get(first_series, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    
    # Check for episode links
    ep_links = soup.find_all("a", href=True)
    ep_count = len([l for l in ep_links if "episode" in l.get("href", "").lower() or "/ep/" in l.get("href", "")])
    print(f"Episode links: {ep_count}")
    
    # Show all links
    print("\nAll links on series page:")
    for link in ep_links[:20]:
        href = link.get("href", "")
        text = link.get_text(strip=True)
        if text and len(text) > 2:
            try:
                print(f"  [{text[:40]}] -> {href}")
            except:
                pass
