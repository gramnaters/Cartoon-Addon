import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - ANIME & EPISODE PAGES")
print("=" * 60)

# Test anime page
anime_url = "https://animelok.xyz/anime/b85ef19d042b"
print(f"\n[1] Anime Page: {anime_url}")
try:
    r = requests.get(anime_url, headers=HEADERS, timeout=15)
    print(f"  Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find episode links
    ep_links = re.findall(r'href=["\']([^"\']*(?:episode|watch)[^"\']*)["\']', r.text, re.I)
    print(f"  Episode links: {list(set(ep_links))[:10]}")
    
    # Find anime title
    title_match = re.search(r'<title>(.*?)</title>', r.text)
    if title_match:
        print(f"  Title: {title_match.group(1)}")
    
    # Find data in scripts
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
    for script in scripts:
        if "self.__next" in script and len(script) > 1000:
            # Try to extract anime data
            data_matches = re.findall(r'"title":"([^"]+)"', script)
            if data_matches:
                print(f"  Titles in data: {data_matches[:5]}")
            
            # Find episode IDs
            ep_matches = re.findall(r'"episodeId":"([^"]+)"', script)
            if ep_matches:
                print(f"  Episode IDs: {ep_matches[:10]}")
            break
except Exception as e:
    print(f"  ERROR: {e}")

# Test search with different format
print("\n[2] Search API")
search_url = "https://animelok.xyz/search?keyword=doraemon"
print(f"  Testing: {search_url}")
try:
    r = requests.get(search_url, headers=HEADERS, timeout=15)
    print(f"  Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find anime links
    anime_links = re.findall(r'href=["\']([^"\']*/anime/[^"\']+)["\']', r.text)
    print(f"  Anime links: {list(set(anime_links))[:10]}")
    
    # Find titles
    titles = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', r.text, re.DOTALL)
    clean_titles = []
    for t in titles:
        clean = re.sub(r'<[^>]+>', '', t).strip()
        if clean and len(clean) > 2:
            clean_titles.append(clean)
    print(f"  Titles: {clean_titles[:10]}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test latest episodes
print("\n[3] Latest Episodes")
latest_url = "https://animelok.xyz/latest-episode"
print(f"  Testing: {latest_url}")
try:
    r = requests.get(latest_url, headers=HEADERS, timeout=15)
    print(f"  Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find episode links
    ep_links = re.findall(r'href=["\']([^"\']*/episode/[^"\']+)["\']', r.text)
    print(f"  Episode links: {list(set(ep_links))[:10]}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test API endpoint
print("\n[4] API Endpoint Test")
api_urls = [
    "https://animelok.xyz/api/search?keyword=naruto",
    "https://animelok.xyz/api/anime",
    "https://animelok.xyz/api/latest",
]

for url in api_urls:
    print(f"\n  Testing: {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"    JSON: {json.dumps(data, indent=2)[:300]}")
            except:
                print(f"    Text: {r.text[:200]}")
    except Exception as e:
        print(f"    ERROR: {e}")
