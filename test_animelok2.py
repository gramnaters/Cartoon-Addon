import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - HTML STRUCTURE")
print("=" * 60)

# Check search page
r = requests.get("https://animelok.xyz/search?keyword=naruto", headers=HEADERS, timeout=15)
print(f"Length: {len(r.text)}")

# Look for script tags with data
scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
print(f"\nScript tags: {len(scripts)}")

for i, script in enumerate(scripts[:10]):
    if len(script) > 100:
        print(f"\nScript {i} (first 300 chars):")
        print(script[:300])

# Look for JSON data in the page
json_matches = re.findall(r'(?:window\.__DATA__|window\.__INITIAL_STATE__|window\.__NEXT_DATA__)\s*=\s*(\{.*?\});', r.text, re.DOTALL)
print(f"\nWindow data matches: {len(json_matches)}")

# Look for data attributes
data_attrs = re.findall(r'data-(?:props|state|initial)\s*=\s*["\']([^"\']+)["\']', r.text)
print(f"\nData attributes: {len(data_attrs)}")

# Check for API calls in scripts
for script in scripts:
    if "fetch" in script or "axios" in script or "api" in script.lower():
        api_matches = re.findall(r'["\']([^"\']*(?:api|fetch|search)[^"\']*)["\']', script, re.I)
        if api_matches:
            print(f"\nAPI calls found: {api_matches[:5]}")

# Look for links to anime pages
links = re.findall(r'href=["\']([^"\']*(?:anime|watch|episode)[^"\']*)["\']', r.text, re.I)
print(f"\nAnime/episode links: {list(set(links))[:10]}")

# Check the home page for Next.js data
print("\n" + "=" * 60)
print("HOME PAGE CHECK")
print("=" * 60)

r = requests.get("https://animelok.xyz/home", headers=HEADERS, timeout=15)

# Check all script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
for i, script in enumerate(scripts):
    if "__NEXT_DATA__" in script:
        print(f"\nFound __NEXT_DATA__ in script {i}")
        data_match = re.search(r'__NEXT_DATA__\s*=\s*(\{.*?\})\s*;?\s*(?:</script>|\n)', script, re.DOTALL)
        if data_match:
            try:
                data = json.loads(data_match.group(1))
                print(f"Parsed successfully!")
                print(f"Keys: {list(data.keys())}")
            except:
                print(f"Could not parse")
        break
    elif "self.__next" in script:
        print(f"\nFound self.__next in script {i}")
        # Extract the data
        data_match = re.search(r'self\.__next_f\.push\(\[.*?"(.*?)"\]\)', script)
        if data_match:
            print(f"Data: {data_match.group(1)[:500]}")
        break
