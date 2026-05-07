import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("PirateXPlay.cc - Structure")
print("=" * 60)

r = requests.get("https://piratexplay.cc", headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

links = soup.find_all("a", href=True)
print(f"Total links: {len(links)}")

for link in links[:30]:
    href = link.get("href", "")
    text = link.get_text(strip=True)
    if text and len(text) > 2:
        try:
            print(f"  [{text}] -> {href}")
        except:
            pass

print("\n" + "=" * 60)
print("Testing search")
print("=" * 60)

r = requests.get("https://piratexplay.cc/?s=doraemon", headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")
links = soup.find_all("a", href=True)
for link in links[:20]:
    href = link.get("href", "")
    text = link.get_text(strip=True)
    if text and len(text) > 2 and "series" in href:
        try:
            print(f"  [{text}] -> {href}")
        except:
            pass

print("\n" + "=" * 60)
print("Testing /series/ page")
print("=" * 60)

r = requests.get("https://piratexplay.cc/series/jujutsu-kaisen-season-3-95479", headers=HEADERS, timeout=15)
print(f"Status: {r.status_code}")
soup = BeautifulSoup(r.text, "html.parser")

# Find iframes
iframes = soup.find_all("iframe")
print(f"Iframes: {len(iframes)}")
for iframe in iframes:
    src = iframe.get("src") or iframe.get("data-src", "")
    print(f"  iframe: {src}")

# Find video tags
videos = soup.find_all("video")
print(f"Video tags: {len(videos)}")

# Find m3u8 in scripts
import re
scripts = soup.find_all("script")
for script in scripts:
    text = script.string or ""
    m3u8 = re.findall(r'["\']([^"\']*\.m3u8[^"\']*)["\']', text)
    if m3u8:
        print(f"Found m3u8: {m3u8[0]}")
