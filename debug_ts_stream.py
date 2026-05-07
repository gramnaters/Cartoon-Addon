import requests, re
from bs4 import BeautifulSoup

# Test ToonStream episode page for streams
url = "https://toonstream.vip/episode/dr-stone-1x1/"
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://toonstream.vip/"}

print(f"Testing: {url}")
r = requests.get(url, headers=headers, timeout=15)
print(f"Status: {r.status_code}")

soup = BeautifulSoup(r.text, "html.parser")

# Find embed page links (?trembed=X&trid=...)
embed_links = re.findall(r'href="(\?trembed=\d+&trid=\d+&trtype=\d+)"', r.text)
print(f"Embed links: {len(embed_links)}")

if embed_links:
    # Try the first embed link
    embed_url = f"{url.split('?')[0]}{embed_links[0]}"
    print(f"Testing embed: {embed_url}")
    
    r2 = requests.get(embed_url, headers={**headers, "Referer": url}, timeout=15)
    print(f"Embed status: {r2.status_code}")
    
    # Find iframes in embed page
    iframes = re.findall(r'<iframe[^>]*src="([^"]+)"', r2.text, re.I)
    print(f"Iframes in embed: {len(iframes)}")
    for i in iframes[:5]:
        print(f"  {i}")
    
    # Try to find m3u8 in embed page
    m3u8s = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r2.text)
    print(f"M3U8 in embed: {len(m3u8s)}")
    for m in m3u8s:
        print(f"  {m}")