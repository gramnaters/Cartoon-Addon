import requests
import re
import json
import logging
from ..config import ANIMELOK_URL, HEADERS

logger = logging.getLogger(__name__)

def get_catalog(page=1, category="anime"):
    # Animelok doesn't have a simple catalog page for Stremio, 
    # we return empty for now or implement it if we find a pattern.
    return []

def search(query):
    # ToonStream/Animelok search is tricky, for now we'll return empty.
    return []

def get_episodes(slug):
    # slug is the anime slug (e.g. 'naruto-20')
    episodes = []
    try:
        url = f"{ANIMELOK_URL}/watch/{slug}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []
        
        # Try to extract totalEpisodes from the page
        # Look for "220" in the text which indicates 220 episodes for Naruto
        total_eps = 0
        
        # Method 1: Look for "totalEpisodes" in scripts
        matches = re.findall(r'totalEpisodes["\']?\s*:\s*(\d+)', response.text)
        if matches:
            total_eps = int(matches[0])
        
        # Method 2: Look for any large number that could be episode count
        if total_eps == 0:
            # Look for patterns like "Episode 1 of 220"
            ep_of_matches = re.findall(r'Episode\s*\d+\s*of\s*(\d+)', response.text, re.I)
            if ep_of_matches:
                total_eps = int(ep_of_matches[0])
        
        # Method 3: Search in self.__next_f.push calls for languageEpisodes
        if total_eps == 0:
            push_calls = re.findall(r'self\.__next_f\.push\((.*?)\)', response.text)
            for call in push_calls:
                if '"languageEpisodes":' in call:
                    # Try to extract language with max episodes
                    lang_matches = re.findall(r'"(\w+)":\s*(\d+)', call)
                    if lang_matches:
                        max_eps = max(int(v) for k, v in lang_matches if v.isdigit())
                        if max_eps > total_eps:
                            total_eps = max_eps
        
        # Fallback: if we can't find the count, create a small set
        if total_eps == 0:
            total_eps = 12  # Create 12 placeholder episodes
            logger.info(f"Could not find episode count for {slug}, using placeholder 12")
        
        # Create episode list based on totalEpisodes
        for i in range(1, total_eps + 1):
            episodes.append({
                "id": f"animelok:{slug}:{i}",
                "title": f"Episode {i}",
                "season": 1,
                "episode": i,
                "url": f"{ANIMELOK_URL}/watch/{slug}?ep={i}",
            })
    except Exception as e:
        logger.error(f"Error getting episodes for {slug}: {e}")
    return episodes

def get_streams(page_url, mediaflow_url="", mediaflow_password=""):
    streams = []
    try:
        # Try to fetch the episode page
        headers = {**HEADERS, "Referer": ANIMELOK_URL}
        r = requests.get(page_url, headers=headers, timeout=10)
        
        if r.status_code != 200:
            return []
        
        text = r.text
        
        # Look for m3u8 URLs in the page
        m3u8_matches = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', text)
        for m in m3u8_matches:
            streams.append({
                "name": "Animelok",
                "title": "🎌 Animelok HLS",
                "url": m,
                "behaviorHints": {"notWebReady": False}
            })
            break
        
        # Look for embedded player iframes
        iframes = re.findall(r'<iframe[^>]*src="([^"]+)"', text, re.I)
        for iframe in iframes[:5]:
            if iframe.startswith("http"):
                streams.append({
                    "name": "Animelok",
                    "title": "🎌 Embed",
                    "url": iframe,
                    "behaviorHints": {"notWebReady": False}
                })
                break
        
        # If nothing found, log and return empty
        if not streams:
            logger.info(f"No streams found for {page_url}")
            
    except Exception as e:
        logger.error(f"Error getting streams for {page_url}: {e}")
    return streams
