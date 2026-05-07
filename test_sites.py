import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("TOONSTREAM.ORG ANALYSIS")
print("=" * 60)

r = requests.get("https://toonstream.org", headers=HEADERS, timeout=15)
print(f"Status: {r.status_code}, Length: {len(r.text)}")

# Find links
links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
content_links = [l for l in links if "/series/" in l or "/movie/" in l or "/anime/" in l or "/cartoon/" in l]
print(f"\nContent links found: {len(content_links)}")
for link in content_links[:10]:
    print(f"  {link}")

# Find API endpoints
api_refs = re.findall(r'["\']([^"\']*(?:api|ajax|fetch|json)[^"\']*)["\']', r.text, re.I)
print(f"\nAPI references: {api_refs[:10]}")

# Check for search
search_refs = re.findall(r'["\']([^"\']*search[^"\']*)["\']', r.text, re.I)
print(f"\nSearch references: {search_refs[:10]}")

# Check categories
print("\n" + "=" * 60)
print("ToonStream.org - Category Pages")
print("=" * 60)

for cat in ["anime", "cartoon", "cartoons", "series", "movie"]:
    url = f"https://toonstream.org/category/{cat}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"\n{cat}: Status {r.status_code}, Length {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 10000:
            articles = re.findall(r'<article', r.text)
            print(f"  Articles: {len(articles)}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("ANIMELOK.XYZ ANALYSIS")
print("=" * 60)

r = requests.get("https://animelok.xyz", headers=HEADERS, timeout=15)
print(f"Status: {r.status_code}, Length: {len(r.text)}")

# Find links
links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
content_links = [l for l in links if "/series/" in l or "/movie/" in l or "/anime/" in l]
print(f"\nContent links found: {len(content_links)}")
for link in content_links[:10]:
    print(f"  {link}")

# Find API endpoints
api_refs = re.findall(r'["\']([^"\']*(?:api|ajax|fetch|json)[^"\']*)["\']', r.text, re.I)
print(f"\nAPI references: {api_refs[:10]}")

# Check categories
print("\n" + "=" * 60)
print("Animelok.xyz - Category Pages")
print("=" * 60)

for cat in ["anime", "series", "movie", "cartoon"]:
    url = f"https://animelok.xyz/category/{cat}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"\n{cat}: Status {r.status_code}, Length {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 10000:
            articles = re.findall(r'<article', r.text)
            print(f"  Articles: {len(articles)}")
    except Exception as e:
        print(f"  ERROR: {e}")
