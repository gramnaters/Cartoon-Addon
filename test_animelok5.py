import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - API & DATA EXTRACTION")
print("=" * 60)

# Check anime page for episode data
anime_url = "https://animelok.xyz/anime/3a4c4c24ae78"  # Naruto
print(f"\n[1] Anime Page: {anime_url}")
try:
    r = requests.get(anime_url, headers=HEADERS, timeout=15)
    print(f"  Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find all script content
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
    
    for i, script in enumerate(scripts):
        if "self.__next" in script and len(script) > 10000:
            print(f"\n  Script {i} length: {len(script)}")
            
            # Try to find episode data
            # Look for patterns like {"id":"xxx","episode":1}
            ep_patterns = re.findall(r'\{"id":"([^"]+)"[^}]*"episode":(\d+)', script)
            if ep_patterns:
                print(f"  Episodes found: {len(ep_patterns)}")
                for ep_id, ep_num in ep_patterns[:5]:
                    print(f"    Episode {ep_num}: {ep_id}")
            
            # Look for watch URLs
            watch_urls = re.findall(r'/watch/([a-f0-9]+)', script)
            if watch_urls:
                print(f"  Watch URLs: {watch_urls[:10]}")
            
            # Look for episode list
            ep_list = re.findall(r'"episodes"\s*:\s*\[(.*?)\]', script, re.DOTALL)
            if ep_list:
                print(f"  Episode list found (first 500 chars): {ep_list[0][:500]}")
            break
except Exception as e:
    print(f"  ERROR: {e}")

# Test different anime pages
print("\n[2] Multiple Anime Pages")
anime_ids = ["3a4c4c24ae78", "4fc41cc8e1dc", "f73122610f56"]
for anime_id in anime_ids:
    url = f"https://animelok.xyz/anime/{anime_id}"
    print(f"\n  Testing: {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        
        # Find watch links
        watch_links = re.findall(r'/watch/([a-f0-9]+)', r.text)
        unique_watches = list(set(watch_links))
        print(f"    Watch links: {unique_watches[:10]}")
        
        # Find episode numbers in watch links
        ep_nums = re.findall(r'/watch/[a-f0-9]+.*?episode[=-](\d+)', r.text, re.I)
        if ep_nums:
            print(f"    Episode numbers: {ep_nums[:10]}")
    except Exception as e:
        print(f"    ERROR: {e}")

# Check for API endpoints in JavaScript
print("\n[3] JavaScript API Detection")
r = requests.get("https://animelok.xyz", headers=HEADERS, timeout=15)

# Find JavaScript files
js_files = re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']', r.text)
print(f"  JS files found: {len(js_files)}")

# Check for API patterns in main page
api_patterns = re.findall(r'["\']([^"\']*(?:api|fetch|endpoint)[^"\']*)["\']', r.text, re.I)
print(f"  API patterns: {list(set(api_patterns))[:10]}")

# Check Next.js build manifest
build_manifest = re.findall(r'/_next/static/([^/"]+)/_buildManifest\.js', r.text)
if build_manifest:
    print(f"  Build ID: {build_manifest[0]}")
