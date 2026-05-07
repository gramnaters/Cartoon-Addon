import requests
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - API Detection")
print("=" * 60)

# Check main page for API endpoints or Next.js data
r = requests.get("https://piratexplay.cc", headers=HEADERS, timeout=15)
text = r.text

# Look for __NEXT_DATA__ or similar
if "__NEXT_DATA__" in text:
    print("Found __NEXT_DATA__!")
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', text)
    if match:
        data = json.loads(match.group(1))
        print(f"Next.js data keys: {list(data.keys())}")
        if "props" in data:
            print(f"Props keys: {list(data['props'].keys())}")
            if "pageProps" in data["props"]:
                print(f"PageProps keys: {list(data['props']['pageProps'].keys())}")
                # Show some of the data
                page_props = data["props"]["pageProps"]
                for key, value in page_props.items():
                    if isinstance(value, list) and len(value) > 0:
                        print(f"\n  {key}: {len(value)} items")
                        print(f"  First item: {json.dumps(value[0], indent=2)[:300]}")
                    elif isinstance(value, dict):
                        print(f"\n  {key}: {json.dumps(value, indent=2)[:300]}")

# Look for API URLs in scripts
print("\n" + "=" * 60)
print("Looking for API URLs in scripts")
print("=" * 60)

scripts = re.findall(r'<script[^>]*src="([^"]*)"', text)
print(f"Found {len(scripts)} script files")

# Check for fetch/axios calls
api_patterns = re.findall(r'(?:fetch|axios|api|endpoint)["\']?\s*[:=]\s*["\']([^"\']+)["\']', text)
for pattern in api_patterns:
    print(f"API pattern: {pattern}")

# Check category page
print("\n" + "=" * 60)
print("Category page API check")
print("=" * 60)

r = requests.get("https://piratexplay.cc/category/series", headers=HEADERS, timeout=15)
text = r.text

if "__NEXT_DATA__" in text:
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', text)
    if match:
        data = json.loads(match.group(1))
        if "props" in data and "pageProps" in data["props"]:
            page_props = data["props"]["pageProps"]
            print(f"PageProps keys: {list(page_props.keys())}")
            for key, value in page_props.items():
                if isinstance(value, list) and len(value) > 0:
                    print(f"\n  {key}: {len(value)} items")
                    print(f"  First item: {json.dumps(value[0], indent=2)[:500]}")
                elif isinstance(value, dict):
                    print(f"\n  {key}: {json.dumps(value, indent=2)[:500]}")

# Check search page
print("\n" + "=" * 60)
print("Search page API check")
print("=" * 60)

r = requests.get("https://piratexplay.cc/?s=naruto", headers=HEADERS, timeout=15)
text = r.text

if "__NEXT_DATA__" in text:
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', text)
    if match:
        data = json.loads(match.group(1))
        if "props" in data and "pageProps" in data["props"]:
            page_props = data["props"]["pageProps"]
            print(f"PageProps keys: {list(page_props.keys())}")
            for key, value in page_props.items():
                if isinstance(value, list) and len(value) > 0:
                    print(f"\n  {key}: {len(value)} items")
                    print(f"  First item: {json.dumps(value[0], indent=2)[:500]}")
                elif isinstance(value, dict):
                    print(f"\n  {key}: {json.dumps(value, indent=2)[:500]}")
