import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.scrapers import piratexplay, toonstream, animelok
from app.config import MEDIAFLOW_URL, MEDIAFLOW_PASSWORD

print("=" * 60)
print("TESTING EACH SCRAPER (fast mode)")
print("=" * 60)

# Test PirateXPlay
print("\n[1] PirateXPlay - Catalog (cartoon)")
try:
    items = piratexplay.get_catalog(page=1, category="cartoon")
    print(f"  Found {len(items)} items")
    for item in items[:3]:
        print(f"    - {item['name']} ({item['id']})")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n[2] PirateXPlay - Search (doraemon)")
try:
    items = piratexplay.search("doraemon")
    print(f"  Found {len(items)} items")
    for item in items[:3]:
        print(f"    - {item['name']} ({item['id']})")
except Exception as e:
    print(f"  ERROR: {e}")

# Test ToonStream
print("\n[3] ToonStream - Catalog (cartoon)")
try:
    items = toonstream.get_catalog(page=1, category="cartoon")
    print(f"  Found {len(items)} items")
    for item in items[:3]:
        print(f"    - {item['name']} ({item['id']})")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n[4] ToonStream - Search (doraemon)")
try:
    items = toonstream.search("doraemon")
    print(f"  Found {len(items)} items")
    for item in items[:3]:
        print(f"    - {item['name']} ({item['id']})")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("TESTING STREAMS")
print("=" * 60)

# Test PirateXPlay streams
print("\n[5] PirateXPlay - Streams")
try:
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
                print(f"    - {s.get('name', 'N/A')}: {s.get('url', 'N/A')[:100]}...")
    else:
        print("  No items found in catalog")
except Exception as e:
    print(f"  ERROR: {e}")

# Test ToonStream streams
print("\n[6] ToonStream - Streams")
try:
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
                print(f"    - {s.get('name', 'N/A')}: {s.get('url', 'N/A')[:100]}...")
    else:
        print("  No items found in catalog")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
