import requests, re

# Test Animelok with proper episode URL
url = "https://animelok.xyz/watch/naruto-20?ep=1"
headers = {"User-Agent": "Mozilla/5.0"}

print(f"Testing: {url}")
r = requests.get(url, headers=headers, timeout=15)
print(f"Status: {r.status_code}, Length: {len(r.text)}")

# Look for video/stream in the page
soup = __import__('bs4').BeautifulSoup(r.text, "html.parser")

# Iframes
iframes = soup.find_all("iframe")
print(f"Iframes: {len(iframes)}")
for i in iframes[:5]:
    print(f"  src: {i.get('src')}")

# Video tags
videos = soup.find_all("video")
print(f"Video tags: {len(videos)}")

# Look for data-src, data-url, etc
data_attrs = soup.find_all(attrs={"data-src": True})
print(f"data-src: {len(data_attrs)}")

# Search for any video URLs in the page
text = r.text
m3u8s = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', text)
print(f"M3U8 in page: {len(m3u8s)}")
for m in m3u8s[:5]:
    print(f"  {m}")

# Check for embed URLs
embeds = re.findall(r'https?://[^\s"\'<>]+/embed/[^\s"\'<>]*', text)
print(f"Embeds: {len(embeds)}")
for e in embeds[:5]:
    print(f"  {e}")

# Check for server data in the page
scripts = soup.find_all("script")
for script in scripts:
    text = script.string or ""
    if any(x in text for x in ['video', 'player', 'stream', 'embed']):
        print(f"\nFound relevant script, checking...")
        if 'as-cdn21' in text or 'vidstreaming' in text or 'rubystm' in text:
            print(f"  Found server: {text[:200]}")