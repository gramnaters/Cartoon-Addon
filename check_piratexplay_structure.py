import requests
from bs4 import BeautifulSoup

def check_page_structure():
    from app.config import PIRATEXPLAY_URL, HEADERS
    
    url = f"{PIRATEXPLAY_URL}/category/series"
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Check for article tags
    articles = soup.find_all("article")
    print(f"Articles: {len(articles)}")
    
    # Check for common class patterns
    items = soup.select(".item")
    print(f".item: {len(items)}")
    
    posts = soup.select(".post")
    print(f".post: {len(posts)}")
    
    # Check for specific patterns
    data_items = soup.select("[data-tmdb]")
    print(f"[data-tmdb]: {len(data_items)}")
    
    # Just get any a tags linking to /series/
    links = soup.find_all("a", href=True)
    series_links = [l for l in links if "/series/" in l.get("href", "")]
    print(f"Links with /series/: {len(series_links)}")
    for l in series_links[:5]:
        print(f"  {l.get('href')} -> {l.get_text(strip=True)[:30]}")

if __name__ == "__main__":
    check_page_structure()