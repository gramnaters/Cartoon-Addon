import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.scrapers import piratexplay, toonstream, animelok
from app.config import MEDIAFLOW_URL, MEDIAFLOW_PASSWORD

print("=" * 60)
print("TESTING EACH SCRAPER")
print("=" * 60)

# Test PirateXPlay
print("\n[1] PirateXPlay - Catalog (cartoon)")
items = piratexplay.get_catalog(page=1, category="cartoon")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[2] PirateXPlay - Catalog (anime)")
items = piratexplay.get_catalog(page=1, category="anime")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[3] PirateXPlay - Search (doraemon)")
items = piratexplay.search("doraemon")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

# Test ToonStream
print("\n[4] ToonStream - Catalog (cartoon)")
items = toonstream.get_catalog(page=1, category="cartoon")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[5] ToonStream - Catalog (anime)")
items = toonstream.get_catalog(page=1, category="anime")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[6] ToonStream - Search (doraemon)")
items = toonstream.search("doraemon")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

# Test Animelok
print("\n[7] Animelok - Catalog (anime)")
items = animelok.get_catalog(page=1, category="anime")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[8] Animelok - Catalog (dubbed)")
items = animelok.get_catalog(page=1, category="dubbed")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

print("\n[9] Animelok - Search (naruto)")
items = animelok.search("naruto")
print(f"  Found {len(items)} items")
for item in items[:3]:
    print(f"    - {item['name']} ({item['id']})")

print("\n" + "=" * 60)
print("TESTING STREAMS (first item from each source)")
print("=" * 60)

# Test streams for first item from each source
print("\n[10] PirateXPlay - Streams")
items = piratexplay.get_catalog(page=1, category="cartoon")
if items:
    slug = items[0]['id'].split(':')[1]
    print(f"  Testing: {items[0]['name']} (slug: {slug})")
    episodes = piratexplay.get_episodes(slug)
    print(f"  Episodes found: {len(episodes)}")
    if episodes:
        streams = piratexplay.get_streams(episodes[0]['url'], MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
        print(f"  Streams found: {len(streams)}")
        for s in streams[:3]:
            print(f"    - {s.get('name', 'N/A')}: {s.get('url', 'N/A')[:80]}...")
else:
    print("  No items found in catalog")

print("\n[11] ToonStream - Streams")
items = toonstream.get_catalog(page=1, category="cartoon")
if items:
    slug = items[0]['id'].split(':')[1]
    print(f"  Testing: {items[0]['name']} (slug: {slug})")
    episodes = toonstream.get_episodes(slug)
    print(f"  Episodes found: {len(episodes)}")
    if episodes:
        streams = toonstream.get_streams(episodes[0]['url'], MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
        print(f"  Streams found: {len(streams)}")
        for s in streams[:3]:
            print(f"    - {s.get('name', 'N/A')}: {s.get('url', 'N/A')[:80]}...")
else:
    print("  No items found in catalog")

print("\n[12] Animelok - Streams")
items = animelok.get_catalog(page=1, category="anime")
if items:
    slug = items[0]['id'].split(':')[1]
    print(f"  Testing: {items[0]['name']} (slug: {slug})")
    episodes = animelok.get_episodes(slug)
    print(f"  Episodes found: {len(episodes)}")
    if episodes:
        streams = animelok.get_streams(episodes[0]['url'], MEDIAFLOW_URL, MEDIAFLOW_PASSWORD)
        print(f"  Streams found: {len(streams)}")
        for s in streams[:3]:
            print(f"    - {s.get('name', 'N/A')}: {s.get('url', 'N/A')[:80]}...")
else:
    print("  No items found in catalog")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
