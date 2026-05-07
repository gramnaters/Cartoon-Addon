import requests
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - Category Page Data Extraction")
print("=" * 60)

for category in ["series", "movie"]:
    url = f"https://piratexplay.cc/category/{category}"
    print(f"\nCategory: {category}")
    r = requests.get(url, headers=HEADERS, timeout=15)
    
    # Find JSON data blocks
    json_matches = re.findall(r'(?:var|let|const)\s+(\w+)\s*=\s*(\{[^;]*\}|\[[^\]]*\]);', r.text)
    print(f"  Found {len(json_matches)} data blocks")
    
    for var_name, json_str in json_matches:
        try:
            data = json.loads(json_str)
            print(f"\n  Variable: {var_name}")
            print(f"  Type: {type(data)}")
            if isinstance(data, list):
                print(f"  Length: {len(data)}")
                if len(data) > 0:
                    print(f"  First item: {json.dumps(data[0], indent=2)[:500]}")
            elif isinstance(data, dict):
                print(f"  Keys: {list(data.keys())}")
                print(f"  Data: {json.dumps(data, indent=2)[:500]}")
        except:
            pass

print("\n" + "=" * 60)
print("Testing episode API")
print("=" * 60)

# Try to get episodes for a series
test_url = "naruto-season-5-46260"
print(f"\nTesting series: {test_url}")

# Check if there's an episode API
api_endpoints = [
    f"https://piratexplay.cc/api/episodes.php?slug={test_url}",
    f"https://piratexplay.cc/api/series.php?slug={test_url}",
    f"https://piratexplay.cc/series/{test_url}",
]

for endpoint in api_endpoints:
    print(f"\n  Testing: {endpoint}")
    try:
        r = requests.get(endpoint, headers=HEADERS, timeout=10)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"    JSON: {json.dumps(data, indent=2)[:500]}")
            except:
                # Check for episode data in HTML
                if "episode" in r.text.lower():
                    print(f"    Contains 'episode' keyword")
                    # Find episode links
                    ep_links = re.findall(r'href=["\']([^"\']*episode[^"\']*)["\']', r.text, re.I)
                    print(f"    Episode links: {ep_links[:5]}")
    except Exception as e:
        print(f"    ERROR: {e}")
