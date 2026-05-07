import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - DATA EXTRACTION")
print("=" * 60)

# Get watch page
watch_url = "https://animelok.xyz/watch/3a4c4c24ae78"
r = requests.get(watch_url, headers=HEADERS, timeout=15)

# Find all self.__next_f.push data
push_data = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text, re.DOTALL)

print(f"\nFound {len(push_data)} data chunks")

# Combine all data
all_data = ""
for chunk in push_data:
    # Unescape the data
    chunk = chunk.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
    all_data += chunk

# Find anime data
anime_match = re.search(r'"anime":\{[^}]*"id":(\d+)[^}]*"title":"([^"]+)"[^}]*"slug":"([^"]+)"[^}]*"totalEpisodes":(\d+)', all_data)
if anime_match:
    print(f"\nAnime found:")
    print(f"  ID: {anime_match.group(1)}")
    print(f"  Title: {anime_match.group(2)}")
    print(f"  Slug: {anime_match.group(3)}")
    print(f"  Total Episodes: {anime_match.group(4)}")

# Find cover image
cover_match = re.search(r'"coverImage":\{[^}]*"large":"([^"]+)"', all_data)
if cover_match:
    print(f"  Cover: {cover_match.group(1)}")

# Find episode data
print("\n" + "=" * 60)
print("EPISODE DATA EXTRACTION")
print("=" * 60)

# Look for episode patterns
ep_patterns = re.findall(r'"episodeNumber":(\d+)', all_data)
print(f"\nEpisode numbers found: {len(ep_patterns)}")
if ep_patterns:
    print(f"  Numbers: {ep_patterns[:20]}")

# Look for episode slugs
ep_slugs = re.findall(r'"episodeSlug":"([^"]+)"', all_data)
print(f"\nEpisode slugs found: {len(ep_slugs)}")
if ep_slugs:
    print(f"  Slugs: {ep_slugs[:10]}")

# Look for language episodes
lang_eps = re.findall(r'"languageEpisodes":\{(.*?)\}', all_data)
print(f"\nLanguage episodes: {len(lang_eps)}")
if lang_eps:
    print(f"  First: {lang_eps[0][:500]}")

# Look for season data
season_data = re.findall(r'"season(?:Number|Name|Id)?"\s*:\s*["\']?([^"\',}]+)', all_data, re.I)
print(f"\nSeason data: {season_data[:10]}")

# Find watch URLs
watch_urls = re.findall(r'/watch/([a-f0-9]+)', all_data)
unique_watches = list(set(watch_urls))
print(f"\nWatch URLs: {unique_watches[:20]}")

# Check for server data
server_data = re.findall(r'"server(?:Name|Url|Id)?"\s*:\s*["\']([^"\']+)', all_data, re.I)
print(f"\nServer data: {server_data[:10]}")

# Check for stream URLs
stream_urls = re.findall(r'https?://[^\s"\'<>]+\.(?:m3u8|mp4)', all_data)
print(f"\nStream URLs: {stream_urls[:5]}")
