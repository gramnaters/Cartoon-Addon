import requests
from bs4 import BeautifulSoup
import logging
import re
import urllib.parse
from ..config import TOONSTREAM_URL, HEADERS

logger = logging.getLogger(__name__)

def get_catalog(page=1, category="cartoon"):
    items = []
    try:
        if category == "cartoon":
            url = f"{TOONSTREAM_URL}/category/cartoon/"
        elif category == "anime":
            url = f"{TOONSTREAM_URL}/category/anime/anime-series/"
        else:
            url = f"{TOONSTREAM_URL}/category/cartoon/"

        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        articles = soup.find_all("article")
        for article in articles:
            try:
                link_el = article.select_one("a")
                title_el = article.select_one("h2") or article.select_one("h3") or article.select_one(".title")
                img_el = article.select_one("img")

                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                link = link_el.get("href", "") if link_el else ""
                poster = img_el.get("src", "") if img_el else ""
                
                if not link or not title:
                    continue
                    
                # Determine type based on URL structure
                item_type = "series"
                if "/movies/" in link:
                    item_type = "movie"
                
                # Extract slug from /series/slug or /movies/slug
                if "/series/" in link:
                    slug = link.split("/series/")[-1].rstrip("/")
                elif "/movies/" in link:
                    slug = link.split("/movies/")[-1].rstrip("/")
                else:
                    slug = link.rstrip("/").split("/")[-1]
                
                stremio_id = f"toonstream:{slug}"

                items.append({
                    "id": stremio_id,
                    "type": item_type,
                    "name": title,
                    "poster": poster,
                    "source": "toonstream",
                    "url": link,
                })
            except Exception as e:
                logger.error(f"ToonStream item parse error: {e}")
    except Exception as e:
        logger.error(f"ToonStream catalog error: {e}")
    return items

def search(query):
    items = []
    try:
        # Use WordPress search
        url = f"{TOONSTREAM_URL}/?s={urllib.parse.quote(query)}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        
        articles = soup.find_all("article")
        for article in articles:
            try:
                link_el = article.select_one("a")
                title_el = article.select_one("h2") or article.select_one("h3")
                img_el = article.select_one("img")
                
                if not title_el:
                    continue
                    
                title = title_el.get_text(strip=True)
                link = link_el.get("href", "") if link_el else ""
                poster = img_el.get("src", "") if img_el else ""
                
                if not link:
                    continue
                
                # Determine type
                item_type = "series"
                if "/movies/" in link:
                    item_type = "movie"
                    
                # Extract slug
                if "/series/" in link:
                    slug = link.split("/series/")[-1].rstrip("/")
                elif "/movies/" in link:
                    slug = link.split("/movies/")[-1].rstrip("/")
                else:
                    slug = link.rstrip("/").split("/")[-1]
                
                items.append({
                    "id": f"toonstream:{slug}",
                    "type": item_type,
                    "name": title,
                    "poster": poster,
                    "source": "toonstream",
                    "url": link,
                })
            except Exception as e:
                logger.error(f"ToonStream search item error: {e}")
    except Exception as e:
        logger.error(f"ToonStream search error: {e}")
    return items

def get_episodes(slug):
    episodes = []
    try:
        url = f"{TOONSTREAM_URL}/series/{slug}/"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        # Find episode links: /episode/{slug}-{season}x{episode}/
        all_links = soup.find_all("a", href=True)
        ep_links = [a for a in all_links if "/episode/" in a.get("href", "") and a.get("href", "").endswith("/")]

        # Sort by episode number
        def extract_ep_num(href):
            match = re.search(r'-(\d+)x(\d+)/$', href)
            if match:
                return (int(match.group(1)), int(match.group(2)))
            return (1, 1)

        ep_links.sort(key=lambda a: extract_ep_num(a.get("href", "")))

        for link in ep_links:
            ep_url = link.get("href", "")
            ep_title = link.get_text(strip=True) or "Episode"
            
            # Extract season and episode from URL
            match = re.search(r'-(\d+)x(\d+)/$', ep_url)
            if match:
                season = int(match.group(1))
                ep_num = int(match.group(2))
            else:
                season = 1
                ep_num = len(episodes) + 1
            
            ep_slug = ep_url.rstrip("/").split("/")[-1]
            
            episodes.append({
                "id": f"toonstream:{slug}:{ep_slug}",
                "title": ep_title,
                "season": season,
                "episode": ep_num,
                "url": ep_url,
            })

        # If no episodes found, treat as movie
        if not episodes:
            episodes.append({
                "id": f"toonstream:{slug}:1",
                "title": "Watch",
                "season": 1,
                "episode": 1,
                "url": url,
            })
    except Exception as e:
        logger.error(f"ToonStream episodes error: {e}")
    return episodes

def get_streams(page_url, mediaflow_url="", mediaflow_password=""):
    streams = []
    try:
        headers = {**HEADERS, "Referer": TOONSTREAM_URL}
        r = requests.get(page_url, headers=headers, timeout=15)
        
        # Find embed links: ?trembed=X&trid=XXX&trtype=2
        embed_links = re.findall(r'href="(\?trembed=\d+&trid=\d+&trtype=\d+)"', r.text)
        
        # Make them absolute URLs
        base_url = page_url.split("?")[0]
        
        for embed_param in embed_links[:4]:  # Try first 4 servers
            embed_url = f"{base_url}{embed_param}"
            
            # Fetch the embed page
            try:
                embed_r = requests.get(embed_url, headers={**headers, "Referer": page_url}, timeout=10)
                
                # Find the iframe src in the embed page
                iframes = re.findall(r'<iframe[^>]*src="([^"]+)"', embed_r.text, re.I)
                
                if iframes:
                    stream_url = iframes[0]
                    
                    # If it's another embed, we try to resolve it or just return as-is
                    # For now, return the direct embed URL
                    streams.append({
                        "name": "ToonStream",
                        "title": "📺 ToonStream",
                        "url": stream_url,
                        "behaviorHints": {"notWebReady": False}
                    })
                    
                    if streams:  # Use first working server
                        break
            except Exception as e:
                logger.error(f"ToonStream embed error: {e}")
        
        # Fallback: look for direct video sources in scripts
        if not streams:
            scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
            for script in scripts:
                m3u8_matches = re.findall(r'["\']([^"\']*\.m3u8[^"\']*)["\']', script)
                for m in m3u8_matches:
                    streams.append({
                        "name": "ToonStream",
                        "title": "📺 ToonStream HLS",
                        "url": m,
                        "behaviorHints": {"notWebReady": False}
                    })
                    break
                if streams:
                    break
    except Exception as e:
        logger.error(f"ToonStream stream error: {e}")
    return streams