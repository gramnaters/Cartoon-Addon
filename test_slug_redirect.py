import requests, re

HEADERS = {"User-Agent": "Mozilla/5.0", "AllowRedirects": "True"}

def test_slug():
    # Test with slug
    r1 = requests.get("https://animelok.xyz/watch/naruto-20", headers=HEADERS, timeout=10)
    print(f"Slug 'naruto-20': {r1.status_code}, Final URL: {r1.url}")
    
    # Test with ID
    r2 = requests.get("https://animelok.xyz/watch/3a4c4c24ae78", headers=HEADERS, timeout=10)
    print(f"ID '3a4c4c24ae78': {r2.status_code}, Final URL: {r2.url}")
    
    # Check both for anime data
    for name, r in [("slug", r1), ("id", r2)]:
        push_calls = re.findall(r'self\.__next_f\.push\((.*?)\)', r.text)
        has_anime = any('"anime":' in c for c in push_calls)
        print(f"  {name}: {len(push_calls)} push calls, has anime: {has_anime}")

if __name__ == "__main__":
    test_slug()