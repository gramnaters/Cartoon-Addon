import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - HTML Structure Analysis")
print("=" * 60)

# Check category page
r = requests.get("https://piratexplay.cc/category/series", headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

# Find all elements with class "item"
items = soup.select(".item")
print(f"\n.item elements: {len(items)}")

# Check what's inside .item elements
for i, item in enumerate(items[:3]):
    print(f"\n--- Item {i+1} ---")
    print(f"  Tag: {item.name}")
    print(f"  Classes: {item.get('class', [])}")
    print(f"  Inner HTML (first 300 chars): {str(item)[:300]}")
    
    # Find links
    links = item.find_all("a", href=True)
    for link in links:
        href = link.get("href", "")
        text = link.get_text(strip=True)
        print(f"  Link: [{text}] -> {href}")

print("\n" + "=" * 60)
print("Search page structure")
print("=" * 60)

r = requests.get("https://piratexplay.cc/?s=naruto", headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

# Find all links
links = soup.find_all("a", href=True)
print(f"\nTotal links: {len(links)}")

# Show all links with their text
for link in links:
    href = link.get("href", "")
    text = link.get_text(strip=True)
    if text and len(text) > 2:
        try:
            print(f"  [{text[:50]}] -> {href}")
        except:
            pass

print("\n" + "=" * 60)
print("Check for JavaScript rendered content")
print("=" * 60)

# Check if content is loaded via JavaScript
scripts = soup.find_all("script")
for script in scripts:
    text = script.string or ""
    if "pageProps" in text or "initialData" in text or "catalog" in text.lower():
        print(f"Found data script: {text[:500]}...")
        break
