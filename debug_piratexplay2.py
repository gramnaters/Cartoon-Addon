import requests
from bs4 import BeautifulSoup

def debug_piratexplay2():
    from app.config import PIRATEXPLAY_URL, HEADERS
    
    url = f"{PIRATEXPLAY_URL}/category/series"
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    scripts = soup.find_all("script")
    
    for i, script in enumerate(scripts):
        text = script.string or ""
        if 'tmdb' in text.lower():
            print(f"=== Script #{i} ===")
            print(text[:2000])
            print("...")
            break

if __name__ == "__main__":
    debug_piratexplay2()