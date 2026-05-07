import requests
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - Episode API")
print("=" * 60)

# Get the series page to find the ID
r = requests.get("https://piratexplay.cc/series/naruto-season-5-46260", headers=HEADERS, timeout=15)

# Look for data-id or similar attributes
id_matches = re.findall(r'data-(?:id|post-id|series-id)\s*=\s*["\'](\d+)["\']', r.text)
print(f"Found IDs: {id_matches}")

# Look for episode API calls in the page
api_calls = re.findall(r'/api/episodes\.php[^"\']*', r.text)
print(f"Episode API calls: {api_calls}")

# Look for JavaScript that loads episodes
js_matches = re.findall(r'(?:fetch|ajax|load)\s*\([^)]*episode[^)]*\)', r.text, re.I)
print(f"Episode loading calls: {js_matches}")

# Check for embedded episode data
ep_data = re.findall(r'(?:var|let|const)\s+(?:episodes?|epData)\s*=\s*(\[[^\]]*\]);', r.text)
if ep_data:
    print(f"Found episode data: {ep_data[0][:500]}")

# Try the episode API with different IDs
print("\n" + "=" * 60)
print("Testing episode API with IDs")
print("=" * 60)

for test_id in ["46260", "1", "100"]:
    url = f"https://piratexplay.cc/api/episodes.php?slug=naruto-season-5-46260&id={test_id}"
    print(f"\n  Testing ID: {test_id}")
    r = requests.get(url, headers=HEADERS, timeout=10)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        try:
            data = r.json()
            print(f"    Response: {json.dumps(data, indent=2)[:500]}")
        except:
            print(f"    Text: {r.text[:300]}")

# Check the episode page
print("\n" + "=" * 60)
print("Testing episode page")
print("=" * 60)

ep_url = "https://piratexplay.cc/episode/naruto-season-5-46260-5x107"
print(f"\nEpisode: {ep_url}")
r = requests.get(ep_url, headers=HEADERS, timeout=15)
print(f"Status: {r.status_code}")
print(f"Length: {len(r.text)}")

# Look for video sources
video_matches = re.findall(r'(?:src|source|file)\s*[:=]\s*["\']([^"\']*\.(?:m3u8|mp4)[^"\']*)["\']', r.text)
print(f"Video sources: {video_matches[:3]}")

# Look for iframes
iframe_matches = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\']', r.text)
print(f"Iframes: {iframe_matches[:3]}")
