import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Check PirateXPlay main page structure
print("=" * 60)
print("PirateXPlay - Main Page Analysis")
print("=" * 60)

r = requests.get("https://piratexplay.com", headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

# Find all links
links = soup.find_all("a", href=True)
print(f"\nTotal links found: {len(links)}")

# Look for content links
content_links = []
for link in links:
    href = link.get("href", "")
    text = link.get_text(strip=True)
    if text and len(text) > 3 and "/" in href and "javascript" not in href.lower():
        content_links.append((href, text))

print(f"\nContent links (first 20):")
for href, text in content_links[:20]:
    print(f"  {text}: {href}")

# Look for images
images = soup.find_all("img")
print(f"\nImages found: {len(images)}")
for img in images[:10]:
    src = img.get("src") or img.get("data-src", "")
    alt = img.get("alt", "")
    if src:
        print(f"  {alt}: {src[:80]}")

# Check for JavaScript data
scripts = soup.find_all("script")
print(f"\nScripts found: {len(scripts)}")
for script in scripts:
    text = script.string or ""
    if "props" in text.lower() or "data" in text.lower() or "pageProps" in text.lower():
        print(f"  Found data script: {text[:200]}...")
        break

print("\n" + "=" * 60)
print("PirateXPlay - Trying different URLs")
print("=" * 60)

test_urls = [
    "https://piratexplay.com/anime",
    "https://piratexplay.com/cartoon",
    "https://piratexplay.com/cartoons",
    "https://piratexplay.com/category/anime",
    "https://piratexplay.com/watch",
]

for url in test_urls:
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        print(f"  {url} -> {r.status_code} (final: {r.url})")
        if r.status_code == 200 and len(r.text) > 10000:
            print(f"    Content length: {len(r.text)} chars - LIKELY HAS CONTENT")
    except Exception as e:
        print(f"  {url} -> ERROR: {e}")
