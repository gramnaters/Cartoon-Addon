import requests
import logging
from .config import TMDB_API_KEY

logger = logging.getLogger(__name__)

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

def search_tmdb(title, media_type="tv"):
    if not TMDB_API_KEY:
        return None
    try:
        url = f"{TMDB_BASE}/search/{media_type}"
        params = {"api_key": TMDB_API_KEY, "query": title, "language": "en-US"}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        results = data.get("results", [])
        if results:
            return results[0]
    except Exception as e:
        logger.error(f"TMDB search error: {e}")
    return None

def get_tmdb_by_imdb(imdb_id):
    if not TMDB_API_KEY:
        return None
    try:
        url = f"{TMDB_BASE}/find/{imdb_id}"
        params = {"api_key": TMDB_API_KEY, "external_source": "imdb_id"}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        results = data.get("tv_results", []) or data.get("movie_results", [])
        if results:
            return results[0]
    except Exception as e:
        logger.error(f"TMDB imdb lookup error: {e}")
    return None

def build_meta(item, media_type="series"):
    return {
        "id": item.get("stremio_id", ""),
        "type": media_type,
        "name": item.get("title", ""),
        "poster": item.get("poster", ""),
        "description": item.get("description", ""),
        "genres": item.get("genres", []),
    }
