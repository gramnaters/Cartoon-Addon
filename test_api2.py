import requests
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - API Discovery")
print("=" * 60)

# Try common API endpoints
api_endpoints = [
    "https://piratexplay.cc/wp-json/wp/v2/posts",
    "https://piratexplay.cc/wp-json/wp/v2/types",
    "https://piratexplay.cc/api/posts",
    "https://piratexplay.cc/api/v1/posts",
    "https://piratexplay.cc/api/search?q=naruto",
    "https://piratexplay.cc/api/catalog",
    "https://piratexplay.cc/api/series",
    "https://piratexplay.cc/wp-json/",
    "https://piratexplay.cc/graphql",
]

for endpoint in api_endpoints:
    print(f"\nTesting: {endpoint}")
    try:
        r = requests.get(endpoint, headers=HEADERS, timeout=10)
        print(f"  Status: {r.status_code}")
        print(f"  Content-Type: {r.headers.get('content-type', 'N/A')}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  JSON response: {json.dumps(data, indent=2)[:300]}")
            except:
                print(f"  Text response (first 200): {r.text[:200]}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("Checking JavaScript files for API patterns")
print("=" * 60)

# Get the main page and find JS files
r = requests.get("https://piratexplay.cc", headers=HEADERS, timeout=15)
import re
js_files = re.findall(r'<script[^>]*src="([^"]*\.js[^"]*)"', r.text)
print(f"Found {len(js_files)} JS files")

for js_url in js_files[:5]:
    if not js_url.startswith("http"):
        js_url = "https://piratexplay.cc" + js_url
    print(f"\nChecking: {js_url}")
    try:
        r = requests.get(js_url, headers=HEADERS, timeout=10)
        # Look for API patterns
        api_matches = re.findall(r'["\']/(api|graphql|wp-json|search|catalog)[^"\']*["\']', r.text)
        if api_matches:
            print(f"  Found API patterns: {api_matches[:5]}")
        
        # Look for fetch calls
        fetch_matches = re.findall(r'fetch\s*\(\s*["\']([^"\']+)["\']', r.text)
        if fetch_matches:
            print(f"  Found fetch calls: {fetch_matches[:5]}")
    except Exception as e:
        print(f"  ERROR: {e}")
