import requests, re
from bs4 import BeautifulSoup

def debug_piratexplay():
    from app.config import PIRATEXPLAY_URL, HEADERS
    
    url = f"{PIRATEXPLAY_URL}/category/series"
    print(f"Fetching: {url}")
    r = requests.get(url, headers=HEADERS, timeout=15)
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    
    soup = BeautifulSoup(r.text, "html.parser")
    scripts = soup.find_all("script")
    
    print(f"Found {len(scripts)} script tags")
    
    for i, script in enumerate(scripts):
        text = script.string or ""
        if 'tmdb' in text.lower():
            print(f"Script #{i} contains 'tmdb', length: {len(text)}")
            # Look for JSON arrays with tmdb
            # Try to find arrays that look like [ {"tmdb": ...} ]
            json_matches = re.findall(r'\[(\{[^]]*"tmdb"[^]]*\})\]', text, re.DOTALL)
            print(f"  Found {len(json_matches)} potential JSON array matches")
            if json_matches:
                print(f"  First match: {json_matches[0][:200]}...")
                break

if __name__ == "__main__":
    debug_piratexplay()