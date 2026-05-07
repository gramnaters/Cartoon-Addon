import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.scrapers import piratexplay
from app.config import MEDIAFLOW_URL, MEDIAFLOW_PASSWORD

print("=" * 60)
print("TESTING PIRATEXPLAY SCRAPER (UPDATED)")
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
items = piratexplay.get_catalog(page=1, category="series")
if items:
    first = items[0]
    slug = first['id'].split(':')[1]
    print(f"\n[5] Episodes for: {first['name']} (slug: {slug})")
    episodes = piratexplay.get_episodes(slug)
    print(f"  Found {len(episodes)} episodes")
    for ep in episodes[:3]:
        print(f"    - {ep['title']} ({ep['id']})")
    
    if episodes:
        print(f"\n[6] Streams for first episode")
        streams = piratexplay.get_streams(episodes[0]['url'], MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
        print(f"  Found {len(streams)} streams")
        for s in streams[:3]:
            print(f"    - {s.get('name', 'N/A')}: {s.get('url', 'N/A')[:100]}...")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
