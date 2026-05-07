import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("TOONSTREAM.ORG - DETAILED ANALYSIS")
print("=" * 60)

# Test WordPress REST API
print("\n[1] WordPress REST API")
api_endpoints = [
    "https://toonstream.org/wp-json/wp/v2/posts",
    "https://toonstream.org/wp-json/wp/v2/posts?per_page=5",
    "https://toonstream.org/wp-json/wp/v2/types",
    "https://toonstream.org/wp-json/",
]

for endpoint in api_endpoints:
    print(f"\n  Testing: {endpoint}")
    try:
        r = requests.get(endpoint, headers=HEADERS, timeout=10)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                if isinstance(data, list):
                    print(f"    Results: {len(data)}")
                    if len(data) > 0:
                        print(f"    First item keys: {list(data[0].keys())}")
                        print(f"    First item: {json.dumps(data[0], indent=2)[:500]}")
                elif isinstance(data, dict):
                    print(f"    Keys: {list(data.keys())}")
            except:
                print(f"    Text: {r.text[:200]}")
    except Exception as e:
        print(f"    ERROR: {e}")

# Test search
print("\n[2] Search")
search_url = "https://toonstream.org/?s=naruto"
print(f"  Testing: {search_url}")
try:
    r = requests.get(search_url, headers=HEADERS, timeout=10)
    print(f"    Status: {r.status_code}, Length: {len(r.text)}")
    articles = re.findall(r'<article[^>]*>(.*?)</article>', r.text, re.DOTALL)
    print(f"    Articles: {len(articles)}")
    
    # Find links in articles
    for article in articles[:2]:
        links = re.findall(r'href=["\']([^"\']+)["\']', article)
        titles = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', article, re.DOTALL)
        print(f"    Links: {links[:3]}")
        print(f"    Titles: {titles[:3]}")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n" + "=" * 60)
print("ANIMELOK.XYZ - DETAILED ANALYSIS")
print("=" * 60)

# Check manifest.json
print("\n[1] Stremio Manifest")
manifest_url = "https://animelok.xyz/manifest.json"
print(f"  Testing: {manifest_url}")
try:
    r = requests.get(manifest_url, headers=HEADERS, timeout=10)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"    Manifest: {json.dumps(data, indent=2)[:1000]}")
except Exception as e:
    print(f"    ERROR: {e}")

# Check main page for content
print("\n[2] Main page content")
r = requests.get("https://animelok.xyz", headers=HEADERS, timeout=15)

# Find all links
links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
print(f"  Total links: {len(links)}")

# Show unique content links
unique_links = list(set(links))
content_links = [l for l in unique_links if len(l) > 10 and not l.startswith('#') and not l.startswith('javascript')]
print(f"  Content links (sample):")
for link in sorted(content_links)[:20]:
    print(f"    {link}")

# Find API endpoints
api_refs = re.findall(r'["\']([^"\']*(?:api|wp-json|graphql)[^"\']*)["\']', r.text, re.I)
print(f"\n  API references: {list(set(api_refs))[:10]}")

# Check for search functionality
search_refs = re.findall(r'["\']([^"\']*search[^"\']*)["\']', r.text, re.I)
print(f"\n  Search references: {list(set(search_refs))[:10]}")
