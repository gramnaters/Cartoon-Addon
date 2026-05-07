import requests, re

def analyze_embed():
    url = 'https://toonstream.vip/?trembed=0&trid=26009&trtype=2'
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://toonstream.vip/episode/dr-stone-1x1/'
    }
    r = requests.get(url, headers=headers)
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    
    # Search for video sources
    m3u8 = re.findall(r'https?://[^\s\"\'<>]+\.m3u8[^\s\"\'<>]*', r.text)
    mp4 = re.findall(r'https?://[^\s\"\'<>]+\.mp4[^\s\"\'<>]*', r.text)
    iframes = re.findall(r'<iframe[^>]*src="([^"]+)"', r.text, re.I)
    
    print(f"M3U8 found: {len(m3u8)}")
    for m in m3u8[:5]: print(f"  {m}")
    print(f"MP4 found: {len(mp4)}")
    for m in mp4[:5]: print(f"  {m}")
    print(f"Embedded iframes: {len(iframes)}")
    for i in iframes[:5]: print(f"  {i}")
    
    # Dump first 3000 chars
    print("\n=== Page content (first 3000 chars) ===")
    print(r.text[:3000])

if __name__ == "__main__":
    analyze_embed()