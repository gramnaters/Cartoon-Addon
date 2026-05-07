import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("ToonStream Analysis")
print("=" * 60)

# Try different ToonStream domains
domains = [
    "https://toonstream.day",
    "https://toonstream.co",
    "https://toonstream.me",
    "https://toonstream.tv",
]

for domain in domains:
    print(f"\nTesting: {domain}")
    try:
        r = requests.get(domain, headers=HEADERS, timeout=10, allow_redirects=True)
        print(f"  Status: {r.status_code}")
        print(f"  Final URL: {r.url}")
        print(f"  Length: {len(r.text)}")
        
        # Check if it's a cloudflare challenge
        if "challenge" in r.text.lower() or "cf-browser-verification" in r.text.lower():
            print("  CLOUDFLARE CHALLENGE DETECTED")
        elif len(r.text) > 5000:
            print("  LIKELY HAS CONTENT")
            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.select("article") or soup.select(".item")
            print(f"  Articles/Items: {len(articles)}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("Animelok Analysis")
print("=" * 60)

domains = [
    "https://animelok.com",
    "https://animelok.cc",
    "https://animelok.me",
]

for domain in domains:
    print(f"\nTesting: {domain}")
    try:
        r = requests.get(domain, headers=HEADERS, timeout=10, allow_redirects=True)
        print(f"  Status: {r.status_code}")
        print(f"  Final URL: {r.url}")
        print(f"  Length: {len(r.text)}")
        
        if "challenge" in r.text.lower() or "cf-browser-verification" in r.text.lower():
            print("  CLOUDFLARE CHALLENGE DETECTED")
        elif len(r.text) > 5000:
            print("  LIKELY HAS CONTENT")
            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.select("article") or soup.select(".item")
            print(f"  Articles/Items: {len(articles)}")
    except Exception as e:
        print(f"  ERROR: {e}")
