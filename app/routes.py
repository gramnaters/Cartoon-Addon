import json
import logging
from flask import Blueprint, jsonify, request, render_template_string
from .config import (
    ADDON_ID, ADDON_NAME, ADDON_VERSION, ADDON_DESCRIPTION,
    MEDIAFLOW_URL, MEDIAFLOW_PASSWORD
)
from .scrapers import piratexplay, toonstream, animelok

logger = logging.getLogger(__name__)
main = Blueprint('main', __name__)

MANIFEST = {
    "id": ADDON_ID,
    "version": ADDON_VERSION,
    "name": ADDON_NAME,
    "description": ADDON_DESCRIPTION,
    "logo": "https://i.imgur.com/your-logo.png",
    "resources": ["catalog", "stream", "meta"],
    "types": ["series", "movie"],
    "idPrefixes": ["piratexplay:", "toonstream:", "animelok:"],
    "catalogs": [
        {
            "id": "piratexplay_cartoons",
            "type": "series",
            "name": "🏴 PirateXPlay Cartoons",
            "extra": [{"name": "search", "isRequired": False}, {"name": "skip"}],
        },
        {
            "id": "piratexplay_anime",
            "type": "series",
            "name": "🏴 PirateXPlay Anime",
            "extra": [{"name": "search", "isRequired": False}, {"name": "skip"}],
        },
        {
            "id": "toonstream_cartoons",
            "type": "series",
            "name": "📺 ToonStream Cartoons",
            "extra": [{"name": "search", "isRequired": False}, {"name": "skip"}],
        },
        {
            "id": "toonstream_anime",
            "type": "series",
            "name": "📺 ToonStream Anime",
            "extra": [{"name": "search", "isRequired": False}, {"name": "skip"}],
        },
        {
            "id": "animelok_anime",
            "type": "series",
            "name": "🎌 Animelok Anime",
            "extra": [{"name": "search", "isRequired": False}, {"name": "skip"}],
        },
        {
            "id": "animelok_dubbed",
            "type": "series",
            "name": "🎌 Animelok Dubbed",
            "extra": [{"name": "search", "isRequired": False}, {"name": "skip"}],
        },
    ],
    "behaviorHints": {
        "configurable": True,
        "configurationRequired": False,
    }
}

def _cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

def _json(data):
    from flask import Response
    resp = Response(json.dumps(data), mimetype="application/json")
    return _cors(resp)

def _items_to_metas(items):
    metas = []
    for item in items:
        metas.append({
            "id": item["id"],
            "type": item.get("type", "series"),
            "name": item["name"],
            "poster": item.get("poster", ""),
        })
    return metas

@main.route("/")
def index():
    install_url = request.host_url + "manifest.json"
    stremio_url = f"stremio://{request.host}/manifest.json"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{ADDON_NAME}</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; text-align: center; padding: 50px; }}
            h1 {{ color: #e94560; font-size: 2.5em; }}
            p {{ color: #aaa; font-size: 1.1em; }}
            .btn {{ display: inline-block; margin: 15px; padding: 15px 30px; border-radius: 8px;
                    text-decoration: none; font-size: 1.1em; font-weight: bold; }}
            .install {{ background: #e94560; color: white; }}
            .manifest {{ background: #0f3460; color: white; }}
            .sources {{ margin-top: 30px; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }}
            .source {{ background: #16213e; padding: 15px 25px; border-radius: 8px; border: 1px solid #e94560; }}
        </style>
    </head>
    <body>
        <h1>🎬 {ADDON_NAME}</h1>
        <p>{ADDON_DESCRIPTION}</p>
        <div class="sources">
            <div class="source">🏴 PirateXPlay</div>
            <div class="source">📺 ToonStream</div>
            <div class="source">🎌 Animelok</div>
        </div>
        <br><br>
        <a href="{stremio_url}" class="btn install">⚡ Install in Stremio</a>
        <a href="/manifest.json" class="btn manifest">📋 Manifest JSON</a>
        <br><br>
        <p style="color:#555">Manifest URL: {install_url}</p>
    </body>
    </html>
    """
    from flask import Response
    return Response(html, mimetype="text/html")

@main.route("/manifest.json")
def manifest():
    return _json(MANIFEST)

@main.route("/catalog/<type>/<catalog_id>.json")
@main.route("/catalog/<type>/<catalog_id>/skip=<int:skip>.json")
@main.route("/catalog/<type>/<catalog_id>/search=<search>.json")
def catalog(type, catalog_id, skip=0, search=None):
    # Also support extra params
    search = search or request.args.get("search")
    skip = skip or int(request.args.get("skip", 0))
    page = (skip // 20) + 1

    metas = []
    try:
        if search:
            if catalog_id.startswith("piratexplay"):
                items = piratexplay.search(search)
            elif catalog_id.startswith("toonstream"):
                items = toonstream.search(search)
            elif catalog_id.startswith("animelok"):
                items = animelok.search(search)
            else:
                items = []
        else:
            if catalog_id == "piratexplay_cartoons":
                items = piratexplay.get_catalog(page=page, category="cartoon")
            elif catalog_id == "piratexplay_anime":
                items = piratexplay.get_catalog(page=page, category="anime")
            elif catalog_id == "toonstream_cartoons":
                items = toonstream.get_catalog(page=page, category="cartoon")
            elif catalog_id == "toonstream_anime":
                items = toonstream.get_catalog(page=page, category="anime")
            elif catalog_id == "animelok_anime":
                items = animelok.get_catalog(page=page, category="anime")
            elif catalog_id == "animelok_dubbed":
                items = animelok.get_catalog(page=page, category="dubbed")
            else:
                items = []

        metas = _items_to_metas(items)
    except Exception as e:
        logger.error(f"Catalog error: {e}")

    return _json({"metas": metas})

@main.route("/meta/<type>/<id>.json")
def meta(type, id):
    meta_data = {
        "id": id,
        "type": type,
        "name": id.split(":")[-1].replace("-", " ").title(),
        "poster": "",
        "description": "",
    }

    try:
        parts = id.split(":")
        source = parts[0]
        slug = parts[1] if len(parts) > 1 else ""

        if source == "piratexplay":
            episodes = piratexplay.get_episodes(slug)
        elif source == "toonstream":
            episodes = toonstream.get_episodes(slug)
        elif source == "animelok":
            episodes = animelok.get_episodes(slug)
        else:
            episodes = []

        videos = []
        for ep in episodes:
            videos.append({
                "id": ep["id"],
                "title": ep["title"],
                "season": 1,
                "episode": ep.get("episode", 1),
                "released": "2024-01-01T00:00:00.000Z",
            })

        meta_data["videos"] = videos
    except Exception as e:
        logger.error(f"Meta error: {e}")

    return _json({"meta": meta_data})

@main.route("/stream/<type>/<id>.json")
def stream(type, id):
    streams = []
    try:
        parts = id.split(":")
        source = parts[0]

        if len(parts) >= 3:
            slug = parts[1]
            ep_slug = parts[2]
            if source == "piratexplay":
                page_url = f"https://piratexplay.com/{ep_slug}/"
                streams = piratexplay.get_streams(page_url, MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
            elif source == "toonstream":
                page_url = f"https://toonstream.day/{ep_slug}/"
                streams = toonstream.get_streams(page_url, MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
            elif source == "animelok":
                page_url = f"https://animelok.com/{ep_slug}/"
                streams = animelok.get_streams(page_url, MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
        elif len(parts) == 2:
            slug = parts[1]
            if source == "piratexplay":
                page_url = f"https://piratexplay.com/{slug}/"
                streams = piratexplay.get_streams(page_url, MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
            elif source == "toonstream":
                page_url = f"https://toonstream.day/{slug}/"
                streams = toonstream.get_streams(page_url, MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
            elif source == "animelok":
                page_url = f"https://animelok.com/{slug}/"
                streams = animelok.get_streams(page_url, MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
    except Exception as e:
        logger.error(f"Stream error: {e}")

    return _json({"streams": streams})
