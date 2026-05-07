import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.stdout.reconfigure(encoding='utf-8')

from app.scrapers import piratexplay
from app.config import MEDIAFLOW_URL, MEDIAFLOW_PASSWORD

print("=" * 60)
print("TESTING COMPLETE PIRATEXPLAY SCRAPER")
print("=" * 60)

print("\n[1] Search (naruto)")
items = piratexplay.search("naruto")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[2] Episodes")
if items:
    first = items[0]
    slug = first['id'].split(':')[1]
    print(f"  Testing: {first['name']} (slug: {slug})")
    episodes = piratexplay.get_episodes(slug)
    print(f"  Found {len(episodes)} episodes")
    for ep in episodes[:3]:
        print(f"    - {ep['title']} (S{ep.get('season', 1)}E{ep.get('episode', 1)})")

print("\n[3] Streams")
if items and episodes:
    print(f"  Testing: {episodes[0]['title']}")
    streams = piratexplay.get_streams(episodes[0]['url'], MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
    print(f"  Found {len(streams)} streams")
    for s in streams[:3]:
        url = s.get('url', 'N/A')
        print(f"    - {s.get('name', 'N/A')}: {url[:80]}...")

print("\n" + "=" * 60)
print("TESTING VIA FLASK APP")
print("=" * 60)

from app import create_app
app = create_app()

with app.test_client() as client:
    # Test search
    print("\n[4] Search via API")
    r = client.get('/catalog/series/piratexplay_series.json?search=doraemon')
    data = r.get_json()
    print(f"  Status: {r.status_code}")
    print(f"  Items: {len(data.get('metas', []))}")
    for item in data.get('metas', [])[:3]:
        print(f"    - {item.get('name')} ({item.get('id')})")
    
    # Test meta (episodes)
    if items:
        first = items[0]
        print(f"\n[5] Episodes via API")
        r = client.get(f'/meta/series/{first["id"]}.json')
        data = r.get_json()
        print(f"  Status: {r.status_code}")
        videos = data.get('meta', {}).get('videos', [])
        print(f"  Episodes: {len(videos)}")
        for ep in videos[:3]:
            print(f"    - {ep.get('title')} (S{ep.get('season', 1)}E{ep.get('episode', 1)})")
    
    # Test streams
    if items and episodes:
        ep_id = episodes[0]['id']
        print(f"\n[6] Streams via API")
        r = client.get(f'/stream/series/{ep_id}.json')
        data = r.get_json()
        print(f"  Status: {r.status_code}")
        streams = data.get('streams', [])
        print(f"  Streams: {len(streams)}")
        for s in streams[:3]:
            url = s.get('url', 'N/A')
            print(f"    - {s.get('name', 'N/A')}: {url[:80]}...")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
