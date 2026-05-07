import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

urls = [
    "https://piratexplay.com",
    "https://piratexplay.com/category/cartoon/",
    "https://toonstream.day",
    "https://toonstream.day/category/cartoons/",
]

for url in urls:
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        print(f"  Status: {r.status_code}")
        print(f"  Final URL: {r.url}")
        print(f"  Content length: {len(r.text)} chars")
        # Check for articles
        if "article" in r.text.lower():
            print("  Contains 'article' tag: YES")
        else:
            print("  Contains 'article' tag: NO")
        # Show first 500 chars
        print(f"  First 500 chars:")
        print(r.text[:500])
    except Exception as e:
        print(f"  ERROR: {e}")
