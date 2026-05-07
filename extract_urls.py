import requests
import re

def extract_urls():
    url = "https://animelok.xyz/watch/3a4c4c24ae78?ep=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers)
    
    urls = re.findall(r'https?://[^\s\"\'<>]+', response.text)
    for u in urls:
        print(u)

if __name__ == "__main__":
    extract_urls()
