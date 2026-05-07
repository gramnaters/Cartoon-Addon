import requests, re
from bs4 import BeautifulSoup

def analyze_episode_page():
    url = 'https://toonstream.vip/episode/dr-stone-1x1/'
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Status: {r.status_code}, Length: {len(r.text)}")

    soup = BeautifulSoup(r.text, 'html.parser')

    # Iframes
    iframes = soup.find_all('iframe')
    print(f"\nIframes: {len(iframes)}")
    for iframe in iframes:
        src = iframe.get('src', '')
        print(f"  src: {src}")
        if src.startswith('/'):
            print(f"  -> full: https://toonstream.vip{src}")

    # Video tags
    videos = soup.find_all('video')
    print(f"\nVideo tags: {len(videos)}")
    for v in videos:
        for s in v.find_all('source'):
            print(f"  source src: {s.get('src', '')}")

    # Data attributes
    data_urls = re.findall(r'(?:data-url|data-src|data-video|data-embed|data-link)="([^"]+)"', r.text)
    print(f"\nData URL attrs: {len(data_urls)}")
    for d in data_urls[:20]:
        print(f"  {d}")

    # Scripts containing video-related data
    scripts = soup.find_all('script')
    print(f"\n=== Relevant Scripts ===")
    for script in scripts:
        text = script.string or ''
        if any(kw in text.lower() for kw in ['embed', 'player', 'm3u8', 'mp4', 'stream', 'video_url', 'source_url', 'aa-tbs']):
            print(f"--- Script ({len(text)} chars) ---")
            print(text[:1500])
            print("...")

    # Look for tab content with video servers
    tabs = soup.find_all(class_=re.compile(r'aa-tbs'))
    print(f"\n=== Tab blocks (aa-tbs) ===")
    for tab in tabs:
        print(f"  Class: {tab.get('class')}")
        inner = str(tab)[:1000]
        print(f"  Inner: {inner}")

    # Look for embedded players
    embeds = soup.find_all(class_=re.compile(r'embed|player|video'))
    print(f"\n=== Embed/Player blocks ===")
    for e in embeds:
        src = e.get('src', '')
        print(f"  Tag: {e.name}, Class: {e.get('class')}, Src: {src}")

if __name__ == "__main__":
    analyze_episode_page()