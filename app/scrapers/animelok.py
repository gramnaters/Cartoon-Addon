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
        # Look for patterns like "220 episodes" or "Episode 1 of 220"
        total_eps = 0
        
        # Look in scripts for totalEpisodes
        matches = re.findall(r'"totalEpisodes":\s*(\d+)', response.text)
        if matches:
            total_eps = int(matches[0])
        
        # Fallback: if we can't find the count, create a small set
        if total_eps == 0:
            total_eps = 10  # Create 10 placeholder episodes
            logger.info(f"Could not find episode count for {slug}, using placeholder 10")
        
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
