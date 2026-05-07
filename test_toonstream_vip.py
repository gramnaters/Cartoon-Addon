import requests, re

def analyze_toonstream():
    r = requests.get('https://toonstream.vip/home/', headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Status: {r.status_code}, Length: {len(r.text)}")

    links = re.findall(r'href="([^"]+)"', r.text)
    toon = [l for l in links if 'toonstream.vip' in l and not any(x in l for x in ['wp-content','wp-json','feed','xmlrpc','wp-login'])]
    other = [l for l in links if l.startswith('/') and not any(x in l for x in ['wp-content','wp-json','wp-','feed','xmlrpc'])]
    print("=== ToonStream Links ===")
    for l in toon[:20]: print(l)
    print("=== Relative Links ===")
    for l in other[:20]: print(l)
    iframes = re.findall(r'<iframe[^>]*src="([^"]+)"', r.text, re.I)
    print(f"=== Iframes ({len(iframes)}) ===")
    for i in iframes[:10]: print(i)
    # look for video/player patterns
    players = re.findall(r'(?:data-url|data-src|data-video|data-embed)="([^"]+)"', r.text)
    print(f"=== Player data attrs ({len(players)}) ===")
    for p in players[:10]: print(p)

if __name__ == "__main__":
    analyze_toonstream()