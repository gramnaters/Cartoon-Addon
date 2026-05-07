import requests
from bs4 import BeautifulSoup
import logging
import re
import urllib.parse
from ..config import PIRATEXPLAY_URL, HEADERS

logger = logging.getLogger(__name__)

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

def _make_absolute(url):
    """Convert relative URL to absolute"""
    if url.startswith("http"):
        return url
    if url.startswith("/"):
        return PIRATEXPLAY_URL + url
    return PIRATEXPLAY_URL + "/" + url

def get_catalog(page=1, category="series"):
    items = []
    try:
        if category in ("series", "cartoon", "anime"):
            url = f"{PIRATEXPLAY_URL}/category/series"
        elif category == "movie":
            url = f"{PIRATEXPLAY_URL}/category/movie"
        else:
            url = f"{PIRATEXPLAY_URL}/category/series"

        r = requests.get(url, headers=HEADERS, timeout=15)
        
        # Extract JSON data from page - look for arrays with tmdb data
        # Try to find JSON data in script tags
        soup = BeautifulSoup(r.text, "html.parser")
        scripts = soup.find_all("script")
        
        for script in scripts:
            text = script.string or ""
            # Look for arrays containing tmdb data
            json_matches = re.findall(r'\[(\{[^]]*"tmdb"[^]]*\})\]', text, re.DOTALL)
            for json_str in json_matches:
                try:
                    import json
                    # Try to parse as JSON array
                    data = json.loads(f"[{json_str}]")
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and "tmdb" in item:
                                tmdb = item["tmdb"]
                                title = tmdb.get("title", "")
                                slug = tmdb.get("url", "")
                                poster_path = tmdb.get("poster", "")
                                item_type = tmdb.get("type", "series")
                                
                                if not title or not slug:
                                    continue
                                
                                poster = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else ""
                                stremio_id = f"piratexplay:{slug}"
                                
                                items.append({
                                    "id": stremio_id,
                                    "type": item_type,
                                    "name": title,
                                    "poster": poster,
                                    "source": "piratexplay",
                                    "url": f"{PIRATEXPLAY_URL}/series/{slug}",
                                })
                except Exception as e:
                    logger.error(f"PirateXPlay parse error: {e}")
    except Exception as e:
        logger.error(f"PirateXPlay catalog error: {e}")
    return items

def search(query):
    items = []
    try:
        url = f"{PIRATEXPLAY_URL}/api/search-ajax.php?keyword={requests.utils.quote(query)}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success" and "data" in data:
                for result in data["data"]:
                    if "tmdb" in result:
                        tmdb = result["tmdb"]
                        title = tmdb.get("title", "")
                        slug = tmdb.get("url", "")
                        poster_path = tmdb.get("poster", "")
                        item_type = tmdb.get("type", "series")
                        
                        if not title or not slug:
                            continue
                        
                        poster = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else ""
                        stremio_id = f"piratexplay:{slug}"
                        
                        items.append({
                            "id": stremio_id,
                            "type": item_type,
                            "name": title,
                            "poster": poster,
                            "source": "piratexplay",
                            "url": f"{PIRATEXPLAY_URL}/series/{slug}",
                        })
    except Exception as e:
        logger.error(f"PirateXPlay search error: {e}")
    return items

def get_episodes(slug):
    episodes = []
    try:
        url = f"{PIRATEXPLAY_URL}/series/{slug}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Find episode links
        all_links = soup.find_all("a", href=True)
        for link in all_links:
            href = link.get("href", "")
            if "/episode/" not in href:
                continue
            
            ep_title = link.get_text(strip=True)
            if not ep_title:
                ep_title = href.split("/")[-2] if href.endswith("/") else href.split("/")[-1]
            
            ep_url = _make_absolute(href)
            ep_slug = href.rstrip("/").split("/")[-1]
            
            # Try to extract season and episode number from slug
            # Format: {series-slug}-{season}x{episode}
            match = re.search(r'(\d+)x(\d+)$', ep_slug)
            if match:
                season = int(match.group(1))
                ep_num = int(match.group(2))
            else:
                season = 1
                ep_num = len(episodes) + 1
            
            episodes.append({
                "id": f"piratexplay:{slug}:{ep_slug}",
                "title": ep_title,
                "season": season,
                "episode": ep_num,
                "url": ep_url,
            })

        # If no episodes found, treat as movie/single
        if not episodes:
            episodes.append({
                "id": f"piratexplay:{slug}:watch",
                "title": "Watch",
                "season": 1,
                "episode": 1,
                "url": f"{PIRATEXPLAY_URL}/series/{slug}",
            })
    except Exception as e:
        logger.error(f"PirateXPlay episodes error: {e}")
    return episodes

def get_streams(page_url, mediaflow_url="", mediaflow_password=""):
    streams = []
    try:
        headers = {**HEADERS, "Referer": PIRATEXPLAY_URL}
        r = requests.get(page_url, headers=headers, timeout=15)
        
        # Find iframes (player URLs)
        iframes = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\']', r.text)
        
        for iframe_url in iframes:
            iframe_url = _make_absolute(iframe_url)
            
            # Get the player page
            try:
                r2 = requests.get(iframe_url, headers={**headers, "Referer": page_url}, timeout=15)
                
                # Extract server options with data-link
                server_pattern = r'data-link=["\']([^"\']+)["\'].*?data-language=["\']([^"\']+)["\']'
                servers = re.findall(server_pattern, r2.text, re.DOTALL)
                
                for server_url, server_name in servers:
                    # Try to extract video from each server
                    video_url = _extract_from_server(server_url, iframe_url)
                    if video_url:
                        if mediaflow_url and mediaflow_password:
                            video_url = _wrap_mediaflow(video_url, mediaflow_url, mediaflow_password, page_url)
                        streams.append({
                            "name": f"PirateXPlay ({server_name})",
                            "title": f"🏴 {server_name}",
                            "url": video_url,
                            "behaviorHints": {"notWebReady": False}
                        })
                        break  # Use first working server
            except Exception as e:
                logger.error(f"Player extraction error: {e}")
        
        # Look for direct video sources in scripts (fallback)
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
        for script in scripts:
            m3u8_matches = re.findall(r'["\']([^"\']*\.m3u8[^"\']*)["\']', script)
            for m in m3u8_matches:
                if mediaflow_url and mediaflow_password:
                    m = _wrap_mediaflow(m, mediaflow_url, mediaflow_password, page_url)
                streams.append({
                    "name": "PirateXPlay",
                    "title": "🏴 PirateXPlay HLS",
                    "url": m,
                    "behaviorHints": {"notWebReady": False}
                })
    except Exception as e:
        logger.error(f"PirateXPlay stream error: {e}")
    return streams

def _extract_from_server(server_url, referer):
    """Extract video URL from server page"""
    try:
        headers = {**HEADERS, "Referer": referer}
        r = requests.get(server_url, headers=headers, timeout=15)
        
        # Find m3u8 URLs
        m3u8_matches = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', r.text)
        if m3u8_matches:
            return m3u8_matches[0]
        
        # Find mp4 URLs
        mp4_matches = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', r.text)
        if mp4_matches:
            return mp4_matches[0]
        
        # Find source/file attributes
        source_matches = re.findall(r'(?:source|file|src)\s*[:=]\s*["\']([^"\']+)["\']', r.text)
        for match in source_matches:
            if match.endswith('.m3u8') or match.endswith('.mp4'):
                return match
    except Exception as e:
        logger.error(f"Server extraction error: {e}")
    return None

def _wrap_mediaflow(stream_url, mediaflow_url, mediaflow_password, referer):
    encoded = urllib.parse.quote(stream_url, safe="")
    encoded_ref = urllib.parse.quote(referer, safe="")
    return f"{mediaflow_url}/proxy/hls/manifest.m3u8?d={encoded}&api_password={mediaflow_password}&h_referer={encoded_ref}&h_origin={urllib.parse.quote(PIRATEXPLAY_URL, safe='')}"
