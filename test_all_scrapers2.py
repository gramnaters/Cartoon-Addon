import sys
sys.path.insert(0, '.')

print("=== Testing PirateXPlay ===")
try:
    from app.scrapers import piratexplay
    catalog = piratexplay.get_catalog(page=1, category="series")
    print(f"Catalog (series): {len(catalog)} items")
    if catalog:
        print(f"  First item: {catalog[0]['name']}, type: {catalog[0]['type']}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing ToonStream ===")
try:
    from app.scrapers import toonstream
    catalog = toonstream.get_catalog(page=1, category="cartoon")
    print(f"Catalog (cartoon): {len(catalog)} items")
    if catalog:
        print(f"  First item: {catalog[0]['name']}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing Animelok ===")
try:
    from app.scrapers import animelok
    # Animelok search is empty
    search = animelok.search("Naruto")
    print(f"Search 'Naruto': {len(search)} items")
    
    # Test episodes - use numeric ID instead of slug
    episodes = animelok.get_episodes("naruto-20")
    print(f"Episodes for 'naruto-20': {len(episodes)} items")
except Exception as e:
    print(f"Error: {e}")

print("\n=== All tests completed ===")