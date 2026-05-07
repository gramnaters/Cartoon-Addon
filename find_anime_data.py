import requests, re, json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def find_anime_data():
    r = requests.get("https://animelok.xyz/watch/3a4c4c24ae78", headers=HEADERS, timeout=10)
    push_calls = re.findall(r'self\.__next_f\.push\((.*?)\)', r.text)
    print(f"Found {len(push_calls)} push calls")
    
    # Look for the pattern with "anime" as a key (not "anime":)
    # The actual pattern from earlier was: 4b:{"anime":{"id":...
    for i, call in enumerate(push_calls):
        # Look for { followed by anime
        if '{"anime"' in call or "'anime'" in call:
            print(f"\n=== Push call #{i} ===")
            print(f"Length: {len(call)}")
            # Show the middle portion of the string
            # Find position of "anime"
            pos = call.find('anime')
            if pos != -1:
                print(f"Context around 'anime': {call[pos-10:pos+100]}")
                
        # Also check for any JSON-like structure with id, title, etc
        if '"id":' in call and '"title":' in call:
            print(f"\n=== Push call #{i} has id and title ===")
            print(f"Length: {len(call)}")
            print(f"First 500: {call[:500]}")

if __name__ == "__main__":
    find_anime_data()