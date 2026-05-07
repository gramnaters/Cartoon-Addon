import os

ADDON_ID = "com.gramnaters.cartoon-addon"
ADDON_NAME = "CartoonStream Addon"
ADDON_VERSION = "1.0.0"
ADDON_DESCRIPTION = "Streams from PirateXPlay, ToonStream and Animelok - Cartoons & Anime in Hindi/English"

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
MEDIAFLOW_URL = os.environ.get("MEDIAFLOW_URL", "https://devonwhite1020-media-proxy.hf.space")
MEDIAFLOW_PASSWORD = os.environ.get("MEDIAFLOW_PASSWORD", "")

PIRATEXPLAY_URL = "https://piratexplay.cc"
TOONSTREAM_URL = "https://toonstream.vip"
ANIMELOK_URL = "https://animelok.xyz"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
