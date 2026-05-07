import requests
from bs4 import BeautifulSoup

# Test ToonStream series page
slug = "dr-stone"
url = f"https://toonstream.vip/series/{slug}/"
headers = {"User-Agent": "Mozilla/5.0"}

print(f"Testing: {url}")
r = requests.get(url, headers=headers, timeout=15)
print(f"Status: {r.status_code}")

soup = BeautifulSoup(r.text, "html.parser")

# Find episode links
all_links = soup.find_all("a", href=True)
ep_links = [a for a in all_links if "/episode/" in a.get("href", "") and a.get("href", "").endswith("/")]

print(f"Episode links: {len(ep_links)}")
for a in ep_links[:10]:
    print(f"  {a.get('href')} -> {a.get_text(strip=True)}")

# Check if it redirects to movie
if "/movies/" in r.url:
    print("It's a movie page!")
    # For movies, look for embed iframes
    iframes = soup.find_all("iframe")
    print(f"Iframes: {len(iframes)}")
    for i in iframes:
        print(f"  {i.get('src')}")