import requests
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print("=" * 60)
print("Debug: Extract Server URLs from Player")
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
    
    # Extract server options with data-link
    server_pattern = r'data-link=["\']([^"\']+)["\'].*?data-language=["\']([^"\']+)["\']'
    servers = re.findall(server_pattern, r.text, re.DOTALL)
    
    print(f"\nFound {len(servers)} servers:")
    for link, name in servers:
        print(f"  {name}: {link}")
    
    # Try to extract video from each server
    print("\n" + "=" * 60)
    print("Testing each server for video URLs")
    print("=" * 60)
    
    for link, name in servers[:3]:  # Test first 3
        print(f"\nServer: {name}")
        print(f"URL: {link}")
        try:
            r = requests.get(link, headers={**HEADERS, "Referer": player_url}, timeout=15)
            print(f"Status: {r.status_code}, Length: {len(r.text)}")
            
            # Find m3u8 URLs
            m3u8_matches = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
            if m3u8_matches:
                print(f"Found m3u8: {m3u8_matches[0]}")
            
            # Find mp4 URLs
            mp4_matches = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r.text)
            if mp4_matches:
                print(f"Found mp4: {mp4_matches[0]}")
            
            # Find source/file attributes
            source_matches = re.findall(r'(?:source|file|src)\s*[:=]\s*["\']([^"\']+)["\']', r.text)
            if source_matches:
                print(f"Found source: {source_matches[0]}")
                
        except Exception as e:
            print(f"Error: {e}")
