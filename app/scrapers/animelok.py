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
        
        # Extract metadata from self.__next_f.push calls
        push_calls = re.findall(r'self\.__next_f\.push\((.*?)\)', response.text)
        
        anime_data = None
        for call in push_calls:
            if '"anime":' in call:
                try:
                    start_idx = call.find('{"anime"')
                    end_idx = call.rfind('}') + 1
                    json_str = call[start_idx:end_idx]
                    json_str = json_str.replace('\\"', '"').replace('\\n', ' ')
                    anime_data = json.loads(json_str)
                    break
                except:
                    continue
        
        if not anime_data:
            return []
        
        data = anime_data.get("anime", {})
        total_eps = data.get("totalEpisodes", 0)
        
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
    # We couldn't find a reliable way to extract streams from Animelok's dynamic player.
    # Returning empty for now.
    return []
