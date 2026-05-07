import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ANIMELOK.XYZ - FULL ANALYSIS")
print("=" * 60)

# Test search
print("\n[1] Search API")
search_url = "https://animelok.xyz/search?keyword=naruto"
print(f"  Testing: {search_url}")
try:
    r = requests.get(search_url, headers=HEADERS, timeout=15)
    print(f"    Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find __NEXT_DATA__
    next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text)
    if next_data_match:
        data = json.loads(next_data_match.group(1))
        print(f"    Next.js data keys: {list(data.keys())}")
        if "props" in data:
            print(f"    Props keys: {list(data['props'].keys())}")
            if "pageProps" in data["props"]:
                page_props = data["props"]["pageProps"]
                print(f"    PageProps keys: {list(page_props.keys())}")
                for key, value in page_props.items():
                    if isinstance(value, list) and len(value) > 0:
                        print(f"\n    {key}: {len(value)} items")
                        print(f"    First item: {json.dumps(value[0], indent=2)[:500]}")
                    elif isinstance(value, dict):
                        print(f"\n    {key}: {json.dumps(value, indent=2)[:500]}")
except Exception as e:
    print(f"    ERROR: {e}")

# Test language pages
print("\n[2] Language Pages")
for lang in ["hindi", "english", "tamil", "telugu"]:
    url = f"https://animelok.xyz/languages/{lang}"
    print(f"\n  Testing: {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"    Status: {r.status_code}, Length: {len(r.text)}")
        
        # Find __NEXT_DATA__
        next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text)
        if next_data_match:
            data = json.loads(next_data_match.group(1))
            if "props" in data and "pageProps" in data["props"]:
                page_props = data["props"]["pageProps"]
                print(f"    PageProps keys: {list(page_props.keys())}")
                for key, value in page_props.items():
                    if isinstance(value, list) and len(value) > 0:
                        print(f"    {key}: {len(value)} items")
                        if len(value) > 0:
                            print(f"    First: {json.dumps(value[0], indent=2)[:300]}")
    except Exception as e:
        print(f"    ERROR: {e}")

# Test home page
print("\n[3] Home Page Data")
url = "https://animelok.xyz/home"
print(f"  Testing: {url}")
try:
    r = requests.get(url, headers=HEADERS, timeout=15)
    print(f"    Status: {r.status_code}, Length: {len(r.text)}")
    
    # Find __NEXT_DATA__
    next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text)
    if next_data_match:
        data = json.loads(next_data_match.group(1))
        if "props" in data and "pageProps" in data["props"]:
            page_props = data["props"]["pageProps"]
            print(f"    PageProps keys: {list(page_props.keys())}")
            for key, value in page_props.items():
                if isinstance(value, list) and len(value) > 0:
                    print(f"\n    {key}: {len(value)} items")
                    print(f"    First: {json.dumps(value[0], indent=2)[:300]}")
                elif isinstance(value, dict):
                    print(f"\n    {key}: {json.dumps(value, indent=2)[:300]}")
except Exception as e:
    print(f"    ERROR: {e}")
