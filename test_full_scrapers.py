import sys
sys.path.insert(0, '.')

from app.scrapers import piratexplay, toonstream, animelok

print("=" * 60)
print("TESTING ALL SCRAPERS - CATALOG, EPISODES, STREAMS")
print("=" * 60)

# === PIRATEXPLAY ===
print("\n### PIRATEXPLAY ###")
try:
    catalog = piratexplay.get_catalog(page=1, category="series")
    print(f"Catalog: {len(catalog)} items")
    if catalog:
        print(f"  First: {catalog[0]['name']} (ID: {catalog[0]['id']})")
        
        # Get episodes for first item
        first_slug = catalog[0]['id'].split(':')[1]
        print(f"  Testing episodes for: {first_slug}")
        episodes = piratexplay.get_episodes(first_slug)
        print(f"  Episodes: {len(episodes)} items")
        if episodes:
            print(f"    First: {episodes[0]}")
            
            # Test streams for first episode
            first_ep_url = episodes[0]['url']
            print(f"    Testing streams for: {first_ep_url}")
            streams = piratexplay.get_streams(first_ep_url, "", "")
            print(f"    Streams: {len(streams)} items")
            if streams:
                print(f"      First stream: {streams[0]}")
except Exception as e:
    print(f"ERROR: {e}")

# === TOONSTREAM ===
print("\n### TOONSTREAM ###")
try:
    catalog = toonstream.get_catalog(page=1, category="cartoon")
    print(f"Catalog: {len(catalog)} items")
    if catalog:
        print(f"  First: {catalog[0]['name']} (ID: {catalog[0]['id']})")
        
        first_slug = catalog[0]['id'].split(':')[1]
        print(f"  Testing episodes for: {first_slug}")
        episodes = toonstream.get_episodes(first_slug)
        print(f"  Episodes: {len(episodes)} items")
        if episodes:
            print(f"    First: {episodes[0]}")
            
            first_ep_url = episodes[0]['url']
            print(f"    Testing streams for: {first_ep_url}")
            streams = toonstream.get_streams(first_ep_url, "", "")
            print(f"    Streams: {len(streams)} items")
            if streams:
                print(f"      First stream: {streams[0]}")
except Exception as e:
    print(f"ERROR: {e}")

# === ANIMELOK ===
print("\n### ANIMELOK ###")
try:
    # Test with known anime
    test_slugs = ["naruto-20", "demon-slayer-1262"]
    
    for slug in test_slugs:
        print(f"Testing: {slug}")
        episodes = animelok.get_episodes(slug)
        print(f"  Episodes: {len(episodes)} items")
        if episodes:
            print(f"    First: {episodes[0]}")
            
            first_ep_url = episodes[0]['url']
            print(f"    Testing streams for: {first_ep_url}")
            streams = animelok.get_streams(first_ep_url, "", "")
            print(f"    Streams: {len(streams)} items")
            if streams:
                print(f"      First stream: {streams[0]}")
            break
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)