import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - EPISODE LOADING")
print("=" * 60)

# Get watch page
watch_url = "https://animelok.xyz/watch/3a4c4c24ae78"
r = requests.get(watch_url, headers=HEADERS, timeout=15)

# Find all data chunks
push_data = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text, re.DOTALL)

# Combine and parse
all_data = ""
for chunk in push_data:
    chunk = chunk.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
    all_data += chunk

print(f"\nTotal data length: {len(all_data)}")

# Find anime object
anime_match = re.search(r'"anime":\{.*?\}(?=\})', all_data, re.DOTALL)
if anime_match:
    anime_str = anime_match.group(0)
    print(f"\nAnime object found (first 1000 chars):")
    print(anime_str[:1000])

# Find all episode-related data
print("\n" + "=" * 60)
print("EPISODE PATTERNS")
print("=" * 60)

# Look for episode arrays
ep_arrays = re.findall(r'"episodes"\s*:\s*\[(.*?)\]', all_data, re.DOTALL)
print(f"\nEpisode arrays: {len(ep_arrays)}")
for i, arr in enumerate(ep_arrays[:3]):
    print(f"\n  Array {i} (first 500 chars):")
    print(f"    {arr[:500]}")

# Look for episode objects
ep_objects = re.findall(r'\{"episodeNumber":(\d+).*?\}', all_data)
print(f"\nEpisode objects: {len(ep_objects)}")
if ep_objects:
    print(f"  Numbers: {ep_objects[:20]}")

# Look for watch URLs with episode info
watch_patterns = re.findall(r'/watch/([^"\';]+);(\d+);', all_data)
print(f"\nWatch patterns: {watch_patterns[:10]}")

# Look for episode slugs
ep_slugs = re.findall(r'"episodeSlug"\s*:\s*"([^"]+)"', all_data)
print(f"\nEpisode slugs: {ep_slugs[:10]}")

# Look for episode titles
ep_titles = re.findall(r'"episodeTitle"\s*:\s*"([^"]+)"', all_data)
print(f"\nEpisode titles: {ep_titles[:10]}")

# Look for season data
season_data = re.findall(r'"seasonNumber"\s*:\s*(\d+)', all_data)
print(f"\nSeason numbers: {season_data[:10]}")

# Look for episode layout
ep_layout = re.findall(r'"episodeLayout"\s*:\s*"([^"]+)"', all_data)
print(f"\nEpisode layout: {ep_layout[:5]}")

# Check for RSC data format
print("\n" + "=" * 60)
print("RSC DATA FORMAT")
print("=" * 60)

# Find RSC chunks
rsc_chunks = re.findall(r'\["\$","([^"]+)"', all_data)
print(f"\nRSC components: {list(set(rsc_chunks))[:20]}")

# Find props
props = re.findall(r'"([^"]+)":\s*\{[^}]*"children"', all_data)
print(f"\nProps with children: {list(set(props))[:20]}")
