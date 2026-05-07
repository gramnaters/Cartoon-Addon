import requests
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("Debug: Catalog JSON Parsing")
print("=" * 60)

r = requests.get("https://piratexplay.cc/category/series", headers=HEADERS, timeout=15)

# Find all JSON-like data blocks
json_matches = re.findall(r'(?:var|let|const)\s+(\w+)\s*=\s*(\[.*?\]);', r.text, re.DOTALL)
print(f"Found {len(json_matches)} data blocks")

for var_name, json_str in json_matches:
    print(f"\nVariable: {var_name}")
    print(f"Raw (first 500 chars): {json_str[:500]}")
    try:
        data = json.loads(json_str)
        print(f"Parsed successfully: {type(data)}")
        if isinstance(data, list):
            print(f"Length: {len(data)}")
            if len(data) > 0:
                print(f"First item: {json.dumps(data[0], indent=2)[:300]}")
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        # Try to fix common issues
        # Remove trailing commas
        fixed = re.sub(r',\s*]', ']', json_str)
        fixed = re.sub(r',\s*}', '}', fixed)
        try:
            data = json.loads(fixed)
            print(f"Fixed and parsed successfully: {type(data)}")
        except:
            print("Could not fix")

print("\n" + "=" * 60)
print("Debug: Stream Extraction")
print("=" * 60)

# Get an episode page
ep_url = "https://piratexplay.cc/episode/naruto-season-5-46260-5x107"
print(f"\nTesting: {ep_url}")
r = requests.get(ep_url, headers=HEADERS, timeout=15)
print(f"Status: {r.status_code}, Length: {len(r.text)}")

# Find iframes
iframes = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\']', r.text)
print(f"Iframes: {iframes}")

# Test player URL
if iframes:
    player_url = iframes[0]
    if not player_url.startswith("http"):
        player_url = "https://piratexplay.cc" + player_url
    print(f"\nTesting player: {player_url}")
    r = requests.get(player_url, headers={**HEADERS, "Referer": ep_url}, timeout=15)
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find video sources
    video_matches = re.findall(r'(?:source|file|src)\s*[:=]\s*["\']([^"\']*\.(?:m3u8|mp4)[^"\']*)["\']', r.text)
    print(f"Video sources: {video_matches}")
    
    # Find all URLs
    url_matches = re.findall(r'https?://[^\s"\'<>]+\.(?:m3u8|mp4)', r.text)
    print(f"URL matches: {url_matches}")
    
    # Show first 1000 chars
    print(f"\nPlayer page (first 1000 chars):")
    print(r.text[:1000])
