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
            url = f"{TOONSTREAM_URL}/category/cartoons/page/{page}/"
        elif category == "anime":
            url = f"{TOONSTREAM_URL}/category/anime/page/{page}/"
        else:
            url = f"{TOONSTREAM_URL}/page/{page}/"

        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        articles = (soup.select("article.item") or
                    soup.select(".item.tvshows") or
                    soup.select(".item.movies") or
                    soup.select("article"))

        for article in articles:
            try:
                title_el = article.select_one("h3 a") or article.select_one("h2 a") or article.select_one(".title a")
                img_el = article.select_one("img")
                link_el = article.select_one("a")

                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                link = link_el.get("href", "") if link_el else ""
                poster = ""
                if img_el:
                    poster = img_el.get("src") or img_el.get("data-src") or img_el.get("data-lazy-src", "")

                slug = link.rstrip("/").split("/")[-1]
                stremio_id = f"toonstream:{slug}"

                items.append({
                    "id": stremio_id,
                    "type": "series",
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
        url = f"{TOONSTREAM_URL}/?s={urllib.parse.quote(query)}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        articles = soup.select("article.item") or soup.select("article")
        for article in articles:
            try:
                title_el = article.select_one("h3 a") or article.select_one("h2 a")
                img_el = article.select_one("img")
                link_el = article.select_one("a")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                link = link_el.get("href", "") if link_el else ""
                poster = ""
                if img_el:
                    poster = img_el.get("src") or img_el.get("data-src", "")
                slug = link.rstrip("/").split("/")[-1]
                items.append({
                    "id": f"toonstream:{slug}",
                    "type": "series",
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
        url = f"{TOONSTREAM_URL}/{slug}/"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        ep_links = (soup.select(".episodios li a") or
                    soup.select("#episodes li a") or
                    soup.select(".episodes li a") or
                    soup.select("a[href*='episode']"))

        for i, link in enumerate(ep_links):
            ep_title = link.get_text(strip=True) or f"Episode {i+1}"
            ep_url = link.get("href", "")
            ep_slug = ep_url.rstrip("/").split("/")[-1]
            episodes.append({
                "id": f"toonstream:{slug}:{ep_slug}",
                "title": ep_title,
                "episode": i + 1,
                "url": ep_url,
            })

        if not episodes:
            episodes.append({
                "id": f"toonstream:{slug}:1",
                "title": "Watch",
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
        soup = BeautifulSoup(r.text, "html.parser")

        iframes = soup.select("iframe")
        for iframe in iframes:
            src = iframe.get("src") or iframe.get("data-src", "")
            if src and "http" in src:
                stream_url = _extract_from_embed(src, headers)
                if stream_url:
                    if mediaflow_url and mediaflow_password:
                        stream_url = _wrap_mediaflow(stream_url, mediaflow_url, mediaflow_password, page_url)
                    streams.append({
                        "name": "ToonStream",
                        "title": "📺 ToonStream",
                        "url": stream_url,
                        "behaviorHints": {"notWebReady": False}
                    })

        scripts = soup.find_all("script")
        for script in scripts:
            text = script.string or ""
            for m in re.findall(r'["\']([^"\']*\.m3u8[^"\']*)["\']', text):
                if mediaflow_url and mediaflow_password:
                    m = _wrap_mediaflow(m, mediaflow_url, mediaflow_password, page_url)
                streams.append({
                    "name": "ToonStream",
                    "title": "📺 ToonStream HLS",
                    "url": m,
                    "behaviorHints": {"notWebReady": False}
                })
    except Exception as e:
        logger.error(f"ToonStream stream error: {e}")
    return streams

def _extract_from_embed(embed_url, headers):
    try:
        r = requests.get(embed_url, headers={**headers, "Referer": TOONSTREAM_URL}, timeout=10)
        text = r.text
        for m in re.findall(r'["\']([^"\']*\.m3u8[^"\']*)["\']', text):
            return m
        for m in re.findall(r'["\']([^"\']*\.mp4[^"\']*)["\']', text):
            return m
    except Exception as e:
        logger.error(f"ToonStream embed extract error: {e}")
    return None

def _wrap_mediaflow(stream_url, mediaflow_url, mediaflow_password, referer):
    encoded = urllib.parse.quote(stream_url, safe="")
    encoded_ref = urllib.parse.quote(referer, safe="")
    return f"{mediaflow_url}/proxy/hls/manifest.m3u8?d={encoded}&api_password={mediaflow_password}&h_referer={encoded_ref}&h_origin={urllib.parse.quote(TOONSTREAM_URL, safe='')}"
