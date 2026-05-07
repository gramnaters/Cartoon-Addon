import requests
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - Search API Test")
print("=" * 60)

# Test the search API
queries = ["naruto", "doraemon", "one piece", "dragon ball"]

for query in queries:
    print(f"\nSearch: {query}")
    url = f"https://piratexplay.cc/api/search-ajax.php?keyword={requests.utils.quote(query)}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"  Status: {r.status_code}")
        print(f"  Content-Type: {r.headers.get('content-type', 'N/A')}")
        
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  Response type: {type(data)}")
                if isinstance(data, list):
                    print(f"  Results: {len(data)}")
                    for item in data[:3]:
                        print(f"    - {json.dumps(item, indent=2)[:200]}")
                elif isinstance(data, dict):
                    print(f"  Keys: {list(data.keys())}")
                    print(f"  Response: {json.dumps(data, indent=2)[:500]}")
            except:
                print(f"  Text: {r.text[:300]}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("Testing catalog pages for data")
print("=" * 60)

# Check if category pages have embedded data
for category in ["series", "movie", "anime", "cartoon"]:
    url = f"https://piratexplay.cc/category/{category}"
    print(f"\nCategory: {category}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        # Look for JSON data in the page
        import re
        json_matches = re.findall(r'(?:var|let|const)\s+\w+\s*=\s*(\{[^;]*\}|\[[^\]]*\]);', r.text)
        if json_matches:
            print(f"  Found {len(json_matches)} JSON data blocks")
            for match in json_matches[:2]:
                try:
                    data = json.loads(match)
                    print(f"    Data: {json.dumps(data, indent=2)[:300]}")
                except:
                    pass
        
        # Check for data attributes
        data_attrs = re.findall(r'data-(?:items|posts|series|content)\s*=\s*["\']([^"\']+)["\']', r.text)
        if data_attrs:
            print(f"  Found data attributes: {data_attrs[:3]}")
    except Exception as e:
        print(f"  ERROR: {e}")
