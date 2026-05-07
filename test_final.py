import sys
sys.path.insert(0, '.')

from app.scrapers import piratexplay, toonstream, animelok

print("=" * 60)
print("FINAL TEST - ALL SCRAPERS")
print("=" * 60)

# === PIRATEXPLAY ===
print("\n### PIRATEXPLAY ###")
try:
    catalog = piratexplay.get_catalog(page=1, category="series")
    print(f"Catalog: {len(catalog)} items")
    if catalog:
        # Use a specific working slug
        slug = "grand-blue-dreaming-season-1-79166"
        print(f"Testing: {slug}")
        episodes = piratexplay.get_episodes(slug)
        print(f"Episodes: {len(episodes)}")
        if episodes:
            print(f"  First: Episode {episodes[0]['episode']}")
            # Test stream
            streams = piratexplay.get_streams(episodes[0]['url'], "", "")
            print(f"Streams: {len(streams)}")
            if streams:
                print(f"  Stream URL: {streams[0].get('url', 'N/A')[:100]}...")
except Exception as e:
    print(f"ERROR: {e}")

# === TOONSTREAM ===
print("\n### TOONSTREAM ###")
try:
    # Test with dr-stone which we know works
    slug = "dr-stone"
    print(f"Testing: {slug}")
    episodes = toonstream.get_episodes(slug)
    print(f"Episodes: {len(episodes)}")
    if episodes:
        print(f"  First: {episodes[0]}")
        # Test stream
        streams = toonstream.get_streams(episodes[0]['url'], "", "")
        print(f"Streams: {len(streams)}")
        if streams:
            print(f"  Stream URL: {streams[0].get('url', 'N/A')[:100]}...")
except Exception as e:
    print(f"ERROR: {e}")

# === ANIMELOK ===
print("\n### ANIMELOK ###")
try:
    slug = "naruto-20"
    print(f"Testing: {slug}")
    episodes = animelok.get_episodes(slug)
    print(f"Episodes: {len(episodes)}")
    if episodes:
        print(f"  First: {episodes[0]}")
        # Test stream
        streams = animelok.get_streams(episodes[0]['url'], "", "")
        print(f"Streams: {len(streams)}")
        if streams:
            print(f"  Stream URL: {streams[0].get('url', 'N/A')[:100]}...")
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)