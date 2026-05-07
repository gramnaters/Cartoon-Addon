import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - EPISODE API DISCOVERY")
print("=" * 60)

# Get watch page and look for API calls
watch_url = "https://animelok.xyz/watch/3a4c4c24ae78"
r = requests.get(watch_url, headers=HEADERS, timeout=15)

# Find JavaScript files
js_files = re.findall(r'src=["\'](/_next/static/chunks/[^"\']+)["\']', r.text)
print(f"\nJS files found: {len(js_files)}")

# Check for API patterns in the page
api_patterns = re.findall(r'["\']([^"\']*(?:api|fetch|episode|stream)[^"\']*)["\']', r.text, re.I)
print(f"\nAPI patterns in page: {list(set(api_patterns))[:20]}")

# Check for RSC endpoints
rsc_endpoints = re.findall(r'["\']([^"\']*(?:rsc|__next|_next)[^"\']*)["\']', r.text)
print(f"\nRSC endpoints: {list(set(rsc_endpoints))[:10]}")

# Test RSC endpoint format
print("\n" + "=" * 60)
print("RSC ENDPOINT TEST")
print("=" * 60)

# Next.js RSC format
rsc_url = "https://animelok.xyz/watch/3a4c4c24ae78?__rsc=1"
print(f"\nTesting: {rsc_url}")
try:
    rsc_headers = {**HEADERS, "RSC": "1"}
    rsc_headers["Next-Router-State-Tree"] = "%5B%22%22%5D"
    r = requests.get(rsc_url, headers=rsc_headers, timeout=15)
    print(f"  Status: {r.status_code}")
    print(f"  Content-Type: {r.headers.get('content-type', 'N/A')}")
    print(f"  Length: {len(r.text)}")
    
    if r.status_code == 200:
        # Look for episode data
        ep_data = re.findall(r'"episodeNumber":\d+', r.text)
        print(f"  Episode data: {ep_data[:10]}")
        
        # Show first 1000 chars
        print(f"\n  First 1000 chars:")
        print(r.text[:1000])
except Exception as e:
    print(f"  ERROR: {e}")

# Test with different headers
print("\n" + "=" * 60)
print("ALTERNATIVE RSC TEST")
print("=" * 60)

# Try with Next-Router-Partial-Data header
rsc_url2 = "https://animelok.xyz/watch/3a4c4c24ae78"
print(f"\nTesting: {rsc_url2}")
try:
    rsc_headers2 = {**HEADERS}
    rsc_headers2["RSC"] = "1"
    rsc_headers2["Next-Router-State-Tree"] = "%5B%22%22%5D"
    rsc_headers2["Next-Url"] = "/watch/3a4c4c24ae78"
    r = requests.get(rsc_url2, headers=rsc_headers2, timeout=15)
    print(f"  Status: {r.status_code}")
    print(f"  Content-Type: {r.headers.get('content-type', 'N/A')}")
    print(f"  Length: {len(r.text)}")
    
    if r.status_code == 200:
        print(f"\n  First 2000 chars:")
        print(r.text[:2000])
except Exception as e:
    print(f"  ERROR: {e}")
