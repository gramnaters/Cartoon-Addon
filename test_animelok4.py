import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - WATCH PAGE ANALYSIS")
print("=" * 60)

# Test watch page
watch_url = "https://animelok.xyz/watch/b85ef19d042b"
print(f"\n[1] Watch Page: {watch_url}")
try:
    r = requests.get(watch_url, headers=HEADERS, timeout=15)
    print(f"  Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find episode links
    ep_links = re.findall(r'href=["\']([^"\']*(?:watch|episode)[^"\']*)["\']', r.text, re.I)
    unique_eps = list(set(ep_links))
    print(f"  Episode links: {unique_eps[:15]}")
    
    # Find video sources
    video_sources = re.findall(r'(?:src|source|file)\s*[:=]\s*["\']([^"\']*\.(?:m3u8|mp4)[^"\']*)["\']', r.text)
    print(f"  Video sources: {video_sources[:5]}")
    
    # Find iframes
    iframes = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\']', r.text)
    print(f"  Iframes: {iframes[:5]}")
    
    # Find player URLs
    player_urls = re.findall(r'["\']([^"\']*(?:player|embed|stream)[^"\']*)["\']', r.text, re.I)
    print(f"  Player URLs: {player_urls[:10]}")
    
    # Find m3u8/mp4 in scripts
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
    for script in scripts:
        m3u8 = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', script)
        mp4 = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', script)
        if m3u8 or mp4:
            print(f"  Found in script - m3u8: {m3u8[:3]}, mp4: {mp4[:3]}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test anime page for episodes
print("\n[2] Anime Page - Episode Extraction")
anime_url = "https://animelok.xyz/anime/b85ef19d042b"
try:
    r = requests.get(anime_url, headers=HEADERS, timeout=15)
    
    # Find all links
    all_links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
    
    # Filter for watch/episode links
    watch_links = [l for l in all_links if '/watch/' in l]
    print(f"  Watch links: {list(set(watch_links))[:15]}")
    
    # Find episode data in scripts
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
    for script in scripts:
        if "self.__next" in script and len(script) > 5000:
            # Find episode-like data
            ep_data = re.findall(r'"(?:episode|ep)[^"]*":\s*(\{[^}]*\})', script, re.I)
            if ep_data:
                print(f"  Episode data: {ep_data[:3]}")
            
            # Find episode numbers
            ep_nums = re.findall(r'"episode(?:Number|Num|#)?"\s*:\s*(\d+)', script)
            if ep_nums:
                print(f"  Episode numbers: {ep_nums[:10]}")
            break
except Exception as e:
    print(f"  ERROR: {e}")

# Test search page structure
print("\n[3] Search Page - Data Extraction")
search_url = "https://animelok.xyz/search?keyword=naruto"
try:
    r = requests.get(search_url, headers=HEADERS, timeout=15)
    
    # Find anime cards/items
    # Look for structured data
    anime_items = re.findall(r'<div[^>]*class="[^"]*anime[^"]*"[^>]*>(.*?)</div>', r.text, re.DOTALL)
    print(f"  Anime items: {len(anime_items)}")
    
    # Find poster images
    posters = re.findall(r'<img[^>]*src=["\']([^"\']*(?:poster|cover|thumb)[^"\']*)["\']', r.text, re.I)
    print(f"  Posters: {posters[:5]}")
    
    # Find anime titles with links
    anime_pattern = r'<a[^>]*href=["\'](/anime/[^"\']+)["\'][^>]*>.*?<h[23][^>]*>(.*?)</h[23]>'
    anime_matches = re.findall(anime_pattern, r.text, re.DOTALL)
    print(f"  Anime with titles: {len(anime_matches)}")
    for link, title in anime_matches[:5]:
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        print(f"    {clean_title}: {link}")
except Exception as e:
    print(f"  ERROR: {e}")
