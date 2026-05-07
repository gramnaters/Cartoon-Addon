import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - SLUG FORMAT TEST")
print("=" * 60)

# Test with slug format
slug_url = "https://animelok.xyz/anime/naruto-20"
print(f"\n[1] Anime by slug: {slug_url}")
try:
    r = requests.get(slug_url, headers=HEADERS, timeout=15)
    print(f"  Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find watch links
    watch_links = re.findall(r'/watch/([a-zA-Z0-9-]+)', r.text)
    unique_watches = list(set(watch_links))
    print(f"  Watch links: {unique_watches[:15]}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test watch page with slug
watch_slug_url = "https://animelok.xyz/watch/naruto-20"
print(f"\n[2] Watch by slug: {watch_slug_url}")
try:
    r = requests.get(watch_slug_url, headers=HEADERS, timeout=15)
    print(f"  Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find episode data
    push_data = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', r.text, re.DOTALL)
    all_data = ""
    for chunk in push_data:
        chunk = chunk.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
        all_data += chunk
    
    # Find anime data
    anime_match = re.search(r'"anime":\{[^}]*"id":(\d+)[^}]*"title":"([^"]+)"[^}]*"slug":"([^"]+)"', all_data)
    if anime_match:
        print(f"  Anime: {anime_match.group(2)} (slug: {anime_match.group(3)})")
    
    # Find episode list
    ep_list = re.findall(r'"episodeNumber":(\d+)', all_data)
    print(f"  Episode numbers: {ep_list[:20]}")
    
    # Find watch URLs with episode info
    watch_urls = re.findall(r'/watch/[^"\']+', all_data)
    print(f"  Watch URLs: {watch_urls[:10]}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test search with slug format
print("\n[3] Search Results - Slug Format")
search_url = "https://animelok.xyz/search?keyword=doraemon"
try:
    r = requests.get(search_url, headers=HEADERS, timeout=15)
    
    # Find anime links with slugs
    anime_links = re.findall(r'href=["\'](/anime/[a-zA-Z0-9-]+)["\']', r.text)
    unique_anime = list(set(anime_links))
    print(f"  Anime links: {unique_anime[:10]}")
    
    # Find titles with links
    pattern = r'<a[^>]*href=["\'](/anime/[a-zA-Z0-9-]+)["\'][^>]*>.*?<h[23][^>]*>(.*?)</h[23]>'
    matches = re.findall(pattern, r.text, re.DOTALL)
    print(f"\n  Anime with titles:")
    for link, title in matches[:10]:
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        print(f"    {clean_title}: {link}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test watch page for episode data
print("\n[4] Watch Page - Episode Data")
watch_url = "https://animelok.xyz/watch/naruto-20"
try:
    r = requests.get(watch_url, headers=HEADERS, timeout=15)
    
    # Find all episode-like patterns
    ep_patterns = re.findall(r'"episode(?:Number|Id|Slug|Name)?"\s*:\s*["\']?([^"\',}]+)', r.text, re.I)
    print(f"  Episode patterns: {ep_patterns[:20]}")
    
    # Find language data
    lang_data = re.findall(r'"languageEpisodes":\{([^}]+)\}', r.text)
    if lang_data:
        print(f"  Language episodes: {lang_data[0]}")
    
    # Find server data
    server_data = re.findall(r'"server(?:Name|Url|Id)?"\s*:\s*["\']([^"\']+)', r.text, re.I)
    print(f"  Server data: {server_data[:10]}")
except Exception as e:
    print(f"  ERROR: {e}")
