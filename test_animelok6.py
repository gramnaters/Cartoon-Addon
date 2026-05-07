import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - WATCH PAGE DEEP ANALYSIS")
print("=" * 60)

# Check watch page
watch_url = "https://animelok.xyz/watch/3a4c4c24ae78"
print(f"\n[1] Watch Page: {watch_url}")
try:
    r = requests.get(watch_url, headers=HEADERS, timeout=15)
    print(f"  Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find all script tags
    scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', r.text)
    print(f"\n  External scripts: {len(scripts)}")
    for script in scripts[:10]:
        print(f"    {script}")
    
    # Find inline scripts with data
    inline_scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
    for i, script in enumerate(inline_scripts):
        if len(script) > 1000:
            print(f"\n  Inline script {i} (first 500 chars):")
            print(f"    {script[:500]}")
            
            # Look for API endpoints
            api_matches = re.findall(r'["\']([^"\']*(?:api|fetch|episode|stream)[^"\']*)["\']', script, re.I)
            if api_matches:
                print(f"    API patterns: {api_matches[:10]}")
except Exception as e:
    print(f"  ERROR: {e}")

# Check for Next.js data fetching
print("\n[2] Next.js Data Fetching")
r = requests.get("https://animelok.xyz/watch/3a4c4c24ae78", headers=HEADERS, timeout=15)

# Look for _next/data endpoints
next_data = re.findall(r'/_next/data/([^"\']+)', r.text)
print(f"  Next.js data endpoints: {next_data[:5]}")

# Look for RSC (React Server Components) endpoints
rsc_matches = re.findall(r'["\']([^"\']*(?:rsc|__next|_next)[^"\']*)["\']', r.text)
print(f"  RSC/Next.js patterns: {list(set(rsc_matches))[:10]}")

# Check for episode data in the page
ep_data = re.findall(r'"episode(?:Id|Number|Num)?"\s*:\s*["\']?([^"\',}]+)', r.text, re.I)
print(f"\n  Episode data: {ep_data[:10]}")

# Check for server URLs
server_urls = re.findall(r'["\']([^"\']*(?:server|source|stream)[^"\']*)["\']', r.text, re.I)
print(f"  Server/stream patterns: {list(set(server_urls))[:10]}")

# Test if there's an API for episodes
print("\n[3] API Endpoint Discovery")
api_patterns = [
    "https://animelok.xyz/api/episodes/3a4c4c24ae78",
    "https://animelok.xyz/api/anime/3a4c4c24ae78",
    "https://animelok.xyz/api/watch/3a4c4c24ae78",
    "https://animelok.xyz/api/v1/anime/3a4c4c24ae78",
    "https://animelok.xyz/api/v1/episodes/3a4c4c24ae78",
]

for url in api_patterns:
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
