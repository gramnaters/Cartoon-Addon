import requests
from bs4 import BeautifulSoup
import re

# Test ToonStream "swapped" slug
slug = "swapped"
url = f"https://toonstream.vip/series/{slug}/"
print(f"Testing: {url}")

r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
print(f"Status: {r.status_code}")

# Check what type of page this is
soup = BeautifulSoup(r.text, "html.parser")

# Look for episode links
ep_links = [a for a in soup.find_all("a", href=True) if "/episode/" in a.get("href", "") and a.get("href", "").endswith("/")]
print(f"Episode links: {len(ep_links)}")

# Look for movie links
movie_links = [a for a in soup.find_all("a", href=True) if "/movies/" in a.get("href", "")]
print(f"Movie links: {len(movie_links)}")
for ml in movie_links[:3]:
    print(f"  {ml.get('href')} -> {ml.get_text(strip=True)}")

# If no episodes, check if it's a movie
if not ep_links:
    print("No episodes found, checking if it's a movie...")
    iframes = soup.find_all("iframe")
    print(f"Iframes on page: {len(iframes)}")
    for i in iframes[:5]:
        src = i.get("src", "")
        print(f"  {src}")

# Let's check what the catalog returned
print("\nLet's check the catalog item type")
items = []
soup2 = BeautifulSoup(r.text, "html.parser")
for article in soup2.find_all("article"):
    link_el = article.select_one("a")
    if link_el:
        link = link_el.get("href", "")
        if "/series/" in link:
            print(f"Found series: {link}")