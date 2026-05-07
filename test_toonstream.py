import requests
import re

def test_toonstream():
    url = "https://toonstream.org"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print("Failed to fetch page")
        return

    links = re.findall(r'href="([^"]+)"', response.text)
    toon_links = [l for l in links if l.startswith('https://toonstream.org/') or l.startswith('/')]
    
    print(f"Found {len(toon_links)} links")
    for link in toon_links[:20]:
        print(link)

if __name__ == "__main__":
    test_toonstream()
