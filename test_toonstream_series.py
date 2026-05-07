import requests, re
from bs4 import BeautifulSoup

def analyze_series_page(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Status: {r.status_code}, Length: {len(r.text)}")

    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Find iframes
    iframes = soup.find_all('iframe')
    print(f"Iframes: {len(iframes)}")
    for iframe in iframes:
        src = iframe.get('src', '')
        print(f"  src: {src}")

    # Find episode links
    all_links = soup.find_all('a', href=True)
    ep_links = [a for a in all_links if 'episode' in a.get('href','').lower() or 'episode' in a.get_text().lower()]
    print(f"Episode links: {len(ep_links)}")
    for a in ep_links[:10]:
        print(f"  {a.get('href')} -> {a.get_text(strip=True)[:50]}")

    # Find video tags
    videos = soup.find_all('video')
    print(f"Video tags: {len(videos)}")
    for v in videos:
        src = v.get('src', '') or (v.find('source') and v.find('source').get('src', ''))
        print(f"  src: {src}")

    # Look for data- attributes with URLs
    data_urls = re.findall(r'(?:data-url|data-src|data-video|data-embed)="([^"]+)"', r.text)
    print(f"Data URL attrs: {len(data_urls)}")
    for d in data_urls[:10]:
        print(f"  {d}")

    # Search for embed/player URLs in scripts
    scripts = soup.find_all('script')
    for script in scripts:
        text = script.string or ''
        if 'embed' in text.lower() or 'player' in text.lower() or 'm3u8' in text.lower():
            print(f"Found relevant script: {text[:500]}")

    # Look for all links that could be episodes (with numbers)
    series_links = [a.get('href') for a in all_links if a.get('href') and url.split('/series/')[-1].strip('/') in a.get('href')]
    print(f"Same-series links: {len(series_links)}")
    for link in series_links[:15]:
        print(f"  {link}")

if __name__ == "__main__":
    analyze_series_page('https://toonstream.vip/series/dr-stone/')