import requests, re, json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def debug_animelok():
    slug = "naruto-20"
    url = f"https://animelok.xyz/watch/{slug}"
    print(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}")
    
    push_calls = re.findall(r'self\.__next_f\.push\((.*?)\)', response.text)
    print(f"Found {len(push_calls)} push calls")
    
    for i, call in enumerate(push_calls):
        if '"anime":' in call:
            print(f"Found 'anime' in push call #{i}")
            print(f"Call content: {call[:500]}...")
            # Try to parse
            try:
                start_idx = call.find('{"anime"')
                # Find the closing brace properly
                # Try to balance braces
                depth = 0
                end_idx = start_idx
                for j, c in enumerate(call[start_idx:], start_idx):
                    if c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1
                    if depth == 0:
                        end_idx = j + 1
                        break
                json_str = call[start_idx:end_idx]
                print(f"JSON substring: {json_str[:200]}...")
                # Replace escaped characters
                json_str_clean = json_str.replace('\\"', '"').replace('\\n', ' ')
                anime_data = json.loads(json_str_clean)
                print(f"Success! Title: {anime_data.get('anime', {}).get('title')}")
                print(f"TotalEpisodes: {anime_data.get('anime', {}).get('totalEpisodes')}")
                break
            except Exception as e:
                print(f"Failed to parse: {e}")

if __name__ == "__main__":
    debug_animelok()