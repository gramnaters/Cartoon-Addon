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
        if '"anime"' in call or '"title"' in call:
            print(f"=== Push call #{i} looks promising ===")
            print(f"Length: {len(call)}")
            # Just look for any interesting JSON-like content
            matches = re.findall(r'"(title|id|totalEpisodes|languageEpisodes)"[^}]+', call)
            print(f"Relevant keys: {matches}")
            print(f"Sample: {call[100:300]}")
            print()

if __name__ == "__main__":
    debug_animelok()