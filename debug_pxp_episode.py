import requests, re
from bs4 import BeautifulSoup

# Test PirateXPlay episode page to find stream
url = "https://piratexplay.cc/episode/grand-blue-dreaming-season-1-79166-1x1/"
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://piratexplay.cc/"}

print("=== PIRATEXPLAY EPISODE PAGE ===")
r = requests.get(url, headers=headers, timeout=15)
print(f"Status: {r.status_code}, Length: {len(r.text)}")

soup = BeautifulSoup(r.text, "html.parser")

# Find iframes
iframes = soup.find_all("iframe")
print(f"Iframes: {len(iframes)}")
for i in iframes[:5]:
    src = i.get("src", "")
    print(f"  src: {src}")

# Find data-link attributes (server links)
data_links = soup.find_all(attrs={"data-link": True})
print(f"\nData-links: {len(data_links)}")
for dl in data_links[:5]:
    print(f"  {dl.get('data-link')}")

# Look for any m3u8/mp4 in scripts
scripts = soup.find_all("script")
for script in scripts:
    text = script.string or ""
    m3u8s = re.findall(r'["\']([^"\']*\.m3u8[^"\']*)["\']', text)
    if m3u8s:
        print(f"\nM3U8 in script: {m3u8s[0]}")

# Look for embed links
embed_links = re.findall(r'href="([^"]*embed[^"]*)"', r.text, re.I)
print(f"\nEmbed links: {len(embed_links)}")
for e in embed_links[:5]:
    print(f"  {e}")

# Try to find server options in the HTML
server_divs = soup.find_all(class_=re.compile(r"server|option|embed", re.I))
print(f"\nServer divs: {len(server_divs)}")
for sd in server_divs[:3]:
    print(f"  {sd.get_text()[:100]}")