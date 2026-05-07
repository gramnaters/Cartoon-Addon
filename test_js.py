import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - JavaScript Analysis")
print("=" * 60)

# Get the custom JS file
r = requests.get("https://piratexplay.cc/public/js/index.js?v=0.0003", headers=HEADERS, timeout=15)
js_content = r.text

print(f"JS file length: {len(js_content)} chars")

# Look for API endpoints
api_patterns = re.findall(r'["\']([^"\']*(?:api|fetch|ajax|search|catalog|series|movie)[^"\']*)["\']', js_content, re.I)
print(f"\nAPI-related patterns found: {len(api_patterns)}")
for pattern in api_patterns[:20]:
    print(f"  {pattern}")

# Look for URL patterns
url_patterns = re.findall(r'["\']/(?:[^"\']*/)["\']', js_content)
print(f"\nURL patterns found: {len(url_patterns)}")
for pattern in url_patterns[:20]:
    print(f"  {pattern}")

# Look for fetch/ajax calls
fetch_patterns = re.findall(r'(?:fetch|\.ajax|\.get|\.post)\s*\([^)]*\)', js_content)
print(f"\nFetch/ajax calls found: {len(fetch_patterns)}")
for pattern in fetch_patterns[:10]:
    print(f"  {pattern[:200]}")

# Show first 2000 chars of JS
print(f"\nFirst 2000 chars of JS:")
print(js_content[:2000])
