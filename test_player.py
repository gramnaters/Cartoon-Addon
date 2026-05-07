import requests
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("Debug: Player Page Analysis")
print("=" * 60)

# Get an episode page
ep_url = "https://piratexplay.cc/episode/naruto-season-5-46260-5x107"
r = requests.get(ep_url, headers=HEADERS, timeout=15)

# Find iframes
iframes = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\']', r.text)
print(f"Episode page iframes: {iframes}")

if iframes:
    player_url = iframes[0]
    if not player_url.startswith("http"):
        player_url = "https://piratexplay.cc" + player_url
    
    print(f"\nPlayer URL: {player_url}")
    r = requests.get(player_url, headers={**HEADERS, "Referer": ep_url}, timeout=15)
    
    # Find inner iframes
    inner_iframes = re.findall(r'<iframe[^>]*(?:src|id)=["\']([^"\']+)["\']', r.text)
    print(f"Inner iframes: {inner_iframes}")
    
    # Find all src attributes
    src_matches = re.findall(r'src=["\']([^"\']+)["\']', r.text)
    print(f"All src attributes: {src_matches}")
    
    # Find JavaScript variables
    js_vars = re.findall(r'(?:var|let|const)\s+(\w+)\s*=\s*["\']([^"\']+)["\']', r.text)
    print(f"JavaScript variables: {js_vars}")
    
    # Find URLs in the page
    url_matches = re.findall(r'https?://[^\s"\'<>]+', r.text)
    print(f"All URLs: {url_matches[:10]}")
    
    # Show full page
    print(f"\nFull player page:")
    print(r.text)
