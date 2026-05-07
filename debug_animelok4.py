import requests, re, json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def debug_animelok_id():
    # Use the ID directly
    anime_id = "3a4c4c24ae78"
    url = f"https://animelok.xyz/watch/{anime_id}"
    print(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}")
    
    push_calls = re.findall(r'self\.__next_f\.push\((.*?)\)', response.text)
    print(f"Found {len(push_calls)} push calls")
    
    for i, call in enumerate(push_calls):
        if '"anime"' in call:
            print(f"Found 'anime' in push call #{i}")
            # Try to find JSON with anime data
            # The format is usually like: 4b:{"anime":{...}}
            if '"anime":{' in call:
                print(f"Found 'anime': {{ in call #{i}")
                # Let's look for the exact pattern
                match = re.search(r'"anime":\s*\{[^}]+\}', call)
                if match:
                    print(f"Match: {match.group(0)[:200]}")
                    
            # Try to extract JSON object using simple approach
            start = call.find('"anime"')
            if start != -1:
                print(f"Found 'anime' at position {start}")
                print(f"Context: {call[start:start+200]}")

if __name__ == "__main__":
    debug_animelok_id()