import sys
sys.path.insert(0, '.')

# Test PirateXPlay
print("=== Testing PirateXPlay ===")
try:
    from app.scrapers import piratexplay
    catalog = piratexplay.get_catalog(page=1, category="series")
    print(f"Catalog (series): {len(catalog)} items")
    if catalog:
        print(f"  First item: {catalog[0]['name']}")
    
    search = piratexplay.search("Naruto")
    print(f"Search 'Naruto': {len(search)} items")
    
    if catalog:
        first_id = catalog[0]['id']
        slug = first_id.split(':')[1]
        print(f"Slug for episodes: {slug}")
        # Can't test get_episodes without knowing if it's a series or movie
        # This might fail if we pick a movie, so skip for now
        print("Skipping episode test due to unknown type")
except Exception as e:
    print(f"Error: {e}")

# Test ToonStream
print("\n=== Testing ToonStream ===")
try:
    from app.scrapers import toonstream
    catalog = toonstream.get_catalog(page=1, category="cartoon")
    print(f"Catalog (cartoon): {len(catalog)} items")
    if catalog:
        print(f"  First item: {catalog[0]['name']}")
    
    # Test search
    search = toonstream.search("Naruto")
    print(f"Search 'Naruto': {len(search)} items")
    
    if catalog:
        first_id = catalog[0]['id']
        slug = first_id.split(':')[1]
        print(f"Testing episodes for: {slug}")
        # episodes = toonstream.get_episodes(slug)
        # print(f"Episodes: {len(episodes)} items")
        print("Skipping episode test")
except Exception as e:
    print(f"Error: {e}")

# Test Animelok
print("\n=== Testing Animelok ===")
try:
    from app.scrapers import animelok
    # Animelok returns empty for catalog currently
    catalog = animelok.get_catalog(page=1, category="anime")
    print(f"Catalog: {len(catalog)} items")
    
    # Animelok search is empty
    search = animelok.search("Naruto")
    print(f"Search 'Naruto': {len(search)} items")
    
    # Test episodes for known anime
    episodes = animelok.get_episodes("naruto-20")
    print(f"Episodes for 'naruto-20': {len(episodes)} items")
    if episodes:
        print(f"  First: {episodes[0]}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== All tests completed ===")