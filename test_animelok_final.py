import requests
import re
import json

def test_animelok():
    url = "https://animelok.xyz/watch/3a4c4c24ae78"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print("Failed to fetch page")
        return

    # Look for the next.js data
    # Next.js usually stores data in <script id="__NEXT_DATA__" type="application/json">
    next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response.text, re.S)
    if next_data:
        print("Found __NEXT_DATA__")
        try:
            data = json.loads(next_data.group(1))
            print(json.dumps(data, indent=2)[:2000])
        except Exception as e:
            print(f"Error parsing JSON: {e}")
    else:
        print("No __NEXT_DATA__ found")
        
    # Also look for the self.__next_f.push patterns
    push_patterns = re.findall(r'self\.__next_f\.push\((.*?)\)', response.text)
    print(f"Found {len(push_patterns)} push patterns")
    
    # Also look for the self.__next_f.push patterns
    push_patterns = re.findall(r'self\.__next_f\.push\((.*?)\)', response.text)
    print(f"Found {len(push_patterns)} push patterns")
    
    all_text = ""
    for p in push_patterns:
        # Remove quotes and escape characters
        text = p.strip().strip('"').replace('\\"', '"').replace('\\n', ' ')
        all_text += text + " "
    
    print("\nSearching for 'Episode' in push patterns...")
    ep_matches = re.findall(r'Episode\s*\d+', all_text, re.I)
    print(f"Found {len(ep_matches)} episode mentions")
    for match in ep_matches[:20]:
        print(match)
    
    # Try to find links that look like episodes inside the push patterns
    links_in_push = re.findall(r'\/watch\/[a-zA-Z0-9-]+', all_text)
    print(f"\nFound {len(links_in_push)} watch links in push patterns")
    for link in links_in_push[:20]:
        print(link)




if __name__ == "__main__":
    test_animelok()
