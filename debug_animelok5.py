import requests, re, json

HEADERS = {"User-Agent": "Mozilla/5.0"}

def debug_animelok():
    anime_id = "3a4c4c24ae78"
    url = f"https://animelok.xyz/watch/{anime_id}"
    print(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS, timeout=10)
    print(f"Status: {response.status_code}")
    
    # Search for the pattern: "anime":{"id":
    text = response.text
    if '"anime":{"id":' in text:
        print("Found anime data pattern in HTML!")
    if '"title":"' in text:
        print("Found title in HTML!")
        
    # Try the RSC endpoint directly
    rsc_url = f"https://animelok.xyz/watch/{anime_id}?__rsc=1"
    rsc_r = requests.get(rsc_url, headers=HEADERS, timeout=10)
    print(f"\nRSC endpoint status: {rsc_r.status_code}")
    print(f"RSC length: {len(rsc_r.text)}")
    
    # Try _next/data endpoint
    data_url = f"https://animelok.xyz/_next/data/9f83eb2648030cf5/watch/{anime_id}.json"
    data_r = requests.get(data_url, headers=HEADERS, timeout=10)
    print(f"\nNext/Data endpoint status: {data_r.status_code}")
    if data_r.status_code == 200:
        try:
            data = data_r.json()
            print(f"Data keys: {list(data.keys())}")
        except:
            print("Failed to parse JSON")

if __name__ == "__main__":
    debug_animelok()