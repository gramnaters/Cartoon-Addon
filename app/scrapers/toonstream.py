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
        # First try series URL
        url = f"{TOONSTREAM_URL}/series/{slug}/"
        r = requests.get(url, headers=HEADERS, timeout=15)
        
        # If 404, try movies URL
        if r.status_code == 404:
            url = f"{TOONSTREAM_URL}/movies/{slug}/"
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

        # If no episodes found, try to find iframes for movie stream
        if not episodes:
            iframes = soup.find_all("iframe")
            if iframes:
                # It's a movie with embed
                for iframe in iframes[:3]:
                    src = iframe.get("src", "")
                    if src and src.startswith("http"):
                        episodes.append({
                            "id": f"toonstream:{slug}:embed",
                            "title": "Watch Movie",
                            "season": 1,
                            "episode": 1,
                            "url": src,
                        })
                        break
            
            # Last resort: return the page URL
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
        from html import unescape
        headers = {**HEADERS, "Referer": TOONSTREAM_URL}
        r = requests.get(page_url, headers=headers, timeout=15)
        
        # Decode HTML entities in the page (e.g., &#038; -> &)
        page_text = unescape(r.text)
        
        # Find iframes that contain trembed - these are the embed pages
        iframes = re.findall(r'<iframe[^>]*src="(https?://[^\s"\'<>]+)"', page_text, re.I)
        
        # Also look for iframes with relative URLs containing trembed
        rel_iframes = re.findall(r'<iframe[^>]*src="([^"]*trembed[^"]*)"', page_text, re.I)
        
        # Make absolute URLs from relative ones and decode HTML entities
        for rel_src in rel_iframes:
            rel_src = unescape(rel_src)  # Decode HTML entities
            if rel_src.startswith("/"):
                iframes.append(TOONSTREAM_URL + rel_src)
            elif rel_src.startswith("?"):
                iframes.append(TOONSTREAM_URL + "/" + rel_src)
        
        # Try each iframe
        for iframe_url in iframes[:4]:
            if not iframe_url or iframe_url.startswith("data:"):
                continue
                
            logger.info(f"Testing ToonStream iframe: {iframe_url}")
            
            try:
                embed_r = requests.get(iframe_url, headers={**headers, "Referer": page_url}, 
                                     timeout=10, allow_redirects=True)
                
                final_url = embed_r.url
                
                # Check if it's a direct stream
                if final_url.endswith('.m3u8') or final_url.endswith('.mp4'):
                    streams.append({
                        "name": "ToonStream",
                        "title": "📺 ToonStream",
                        "url": final_url,
                        "behaviorHints": {"notWebReady": False}
                    })
                    continue
                
                # Look for m3u8 in the embed page
                m3u8_matches = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', embed_r.text)
                if m3u8_matches:
                    streams.append({
                        "name": "ToonStream",
                        "title": "📺 ToonStream HLS",
                        "url": m3u8_matches[0],
                        "behaviorHints": {"notWebReady": False}
                    })
                    continue
                
                # Look for nested iframes
                nested_iframes = re.findall(r'<iframe[^>]*src="(https?://[^\s"\'<>]+)"', embed_r.text, re.I)
                for n_if in nested_iframes[:2]:
                    if n_if.startswith("http"):
                        streams.append({
                            "name": "ToonStream",
                            "title": "📺 ToonStream Embed",
                            "url": n_if,
                            "behaviorHints": {"notWebReady": False}
                        })
                        break
                        
                if streams:
                    break
                    
            except Exception as e:
                logger.error(f"ToonStream iframe error: {e}")
        
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