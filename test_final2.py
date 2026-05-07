import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.stdout.reconfigure(encoding='utf-8')

from app.scrapers import piratexplay
from app.config import MEDIAFLOW_URL, MEDIAFLOW_PASSWORD

print("=" * 60)
print("TESTING UPDATED PIRATEXPLAY SCRAPER")
print("=" * 60)

print("\n[1] Catalog (series)")
items = piratexplay.get_catalog(page=1, category="series")
print(f"  Found {len(items)} items")
for item in items[:5]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[2] Catalog (movie)")
items = piratexplay.get_catalog(page=1, category="movie")
print(f"  Found {len(items)} items")
for item in items[:5]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[3] Search (naruto)")
items = piratexplay.search("naruto")
print(f"  Found {len(items)} items")
for item in items[:5]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[4] Search (doraemon)")
items = piratexplay.search("doraemon")
print(f"  Found {len(items)} items")
for item in items[:5]:
    print(f"    - {item['name']} ({item['id']})")

print("\n" + "=" * 60)
print("TESTING EPISODES & STREAMS")
print("=" * 60)

# Get first series and test episodes
items = piratexplay.search("naruto")
if items:
    first = items[0]
    slug = first['id'].split(':')[1]
    print(f"\n[5] Episodes for: {first['name']} (slug: {slug})")
    episodes = piratexplay.get_episodes(slug)
    print(f"  Found {len(episodes)} episodes")
    for ep in episodes[:5]:
        print(f"    - {ep['title']} (S{ep.get('season', 1)}E{ep.get('episode', 1)}) ({ep['id']})")
    
    if episodes:
        print(f"\n[6] Streams for first episode")
        streams = piratexplay.get_streams(episodes[0]['url'], MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
        print(f"  Found {len(streams)} streams")
        for s in streams[:3]:
            url = s.get('url', 'N/A')
            print(f"    - {s.get('name', 'N/A')}: {url[:100]}...")

print("\n" + "=" * 60)
print("TESTING END-TO-END (via Flask app)")
print("=" * 60)

# Start Flask app and test
from app import create_app
app = create_app()

with app.test_client() as client:
    # Test manifest
    print("\n[7] Manifest")
    r = client.get('/manifest.json')
    data = r.get_json()
    print(f"  Status: {r.status_code}")
    print(f"  Addon: {data.get('name')}")
    print(f"  Catalogs: {len(data.get('catalogs', []))}")
    
    # Test catalog
    print("\n[8] Catalog (series)")
    r = client.get('/catalog/series/piratexplay_series.json')
    data = r.get_json()
    print(f"  Status: {r.status_code}")
    print(f"  Items: {len(data.get('metas', []))}")
    for item in data.get('metas', [])[:3]:
        print(f"    - {item.get('name')} ({item.get('id')})")
    
    # Test search
    print("\n[9] Search (doraemon)")
    r = client.get('/catalog/series/piratexplay_series.json?search=doraemon')
    data = r.get_json()
    print(f"  Status: {r.status_code}")
    print(f"  Items: {len(data.get('metas', []))}")
    for item in data.get('metas', [])[:3]:
        print(f"    - {item.get('name')} ({item.get('id')})")
    
    # Test meta (episodes)
    if items:
        first = items[0]
        print(f"\n[10] Meta (episodes for {first['name']})")
        r = client.get(f'/meta/series/{first["id"]}.json')
        data = r.get_json()
        print(f"  Status: {r.status_code}")
        videos = data.get('meta', {}).get('videos', [])
        print(f"  Episodes: {len(videos)}")
        for ep in videos[:3]:
            print(f"    - {ep.get('title')} (S{ep.get('season', 1)}E{ep.get('episode', 1)})")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
