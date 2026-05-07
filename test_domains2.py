import requests
import re
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

print("=" * 60)
print("TOONSTREAM ANALYSIS")
print("=" * 60)

# Test main domain
domains = [
    "https://toonstream.day",
    "https://toonstream.co",
    "https://toonstream.me",
    "https://toonstream.tv",
    "https://toonstream.xyz",
    "https://toonstream.org",
    "https://toonstream.net",
    "https://toonstream.cc",
]

for domain in domains:
    print(f"\nTesting: {domain}")
    try:
        r = requests.get(domain, headers=HEADERS, timeout=8, allow_redirects=True)
        print(f"  Status: {r.status_code}")
        print(f"  Final URL: {r.url}")
        print(f"  Length: {len(r.text)}")
        
        # Check if it's a cloudflare challenge
        if "challenge" in r.text.lower() or "cf-browser-verification" in r.text.lower():
            print("  CLOUDFLARE CHALLENGE")
        elif len(r.text) > 10000:
            print("  LIKELY HAS CONTENT")
            # Check for articles
            if "article" in r.text.lower():
                print("  Contains 'article' tag")
            # Check for API endpoints
            if "api" in r.text.lower():
                print("  Contains 'api' references")
    except requests.exceptions.ConnectTimeout:
        print("  TIMEOUT (connection)")
    except requests.exceptions.ReadTimeout:
        print("  TIMEOUT (read)")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("ANIMELOK ANALYSIS")
print("=" * 60)

domains = [
    "https://animelok.com",
    "https://animelok.cc",
    "https://animelok.me",
    "https://animelok.net",
    "https://animelok.org",
    "https://animelok.xyz",
    "https://anime-lok.com",
    "https://animelok.co",
]

for domain in domains:
    print(f"\nTesting: {domain}")
    try:
        r = requests.get(domain, headers=HEADERS, timeout=8, allow_redirects=True)
        print(f"  Status: {r.status_code}")
        print(f"  Final URL: {r.url}")
        print(f"  Length: {len(r.text)}")
        
        if "challenge" in r.text.lower() or "cf-browser-verification" in r.text.lower():
            print("  CLOUDFLARE CHALLENGE")
        elif len(r.text) > 10000:
            print("  LIKELY HAS CONTENT")
    except requests.exceptions.ConnectTimeout:
        print("  TIMEOUT (connection)")
    except requests.exceptions.ReadTimeout:
        print("  TIMEOUT (read)")
    except Exception as e:
        print(f"  ERROR: {e}")
