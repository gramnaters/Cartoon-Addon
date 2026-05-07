import requests, re, json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def debug_animelok():
    slug = "naruto-20"
    url = f"https://animelok.xyz/watch/{slug}"
    print(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print("Failed to fetch page")
        return
    
    # Extract metadata from self.__next_f.push calls
    push_calls = re.findall(r'self\.__next_f\.push\((.*?)\)', response.text)
    print(f"Found {len(push_calls)} push calls")
    
    anime_data = None
    for call in push_calls:
        if '"anime":' in call:
            try:
                start_idx = call.find('{"anime"')
                end_idx = call.rfind('}') + 1
                json_str = call[start_idx:end_idx]
                json_str = json_str.replace('\\"', '"').replace('\\n', ' ')
                anime_data = json.loads(json_str)
                print(f"Found anime data!")
                print(f"  Title: {anime_data.get('anime', {}).get('title')}")
                print(f"  TotalEpisodes: {anime_data.get('anime', {}).get('totalEpisodes')}")
                break
            except Exception as e:
                print(f"Error parsing: {e}")

if __name__ == "__main__":
    debug_animelok()