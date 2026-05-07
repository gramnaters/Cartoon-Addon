import requests, json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def debug_rsc():
    anime_id = "3a4c4c24ae78"
    url = f"https://animelok.xyz/watch/{anime_id}?__rsc=1"
    response = requests.get(url, headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}, Length: {len(response.text)}")
    
    # Try to parse as JSON
    try:
        data = response.json()
        print(f"JSON keys: {list(data.keys())}")
        print(f"Data: {str(data)[:1000]}")
    except:
        # Not JSON, maybe plain text
        print(f"Not JSON. First 2000 chars: {response.text[:2000]}")

if __name__ == "__main__":
    debug_rsc()