import requests, re

r = requests.get('https://animelok.xyz/watch/naruto-20', headers={'User-Agent': 'Mozilla/5.0'})
push_calls = re.findall(r'self\.__next_f\.push\((.*?)\)', r.text)

print(f"Found {len(push_calls)} push calls")

# Look for totalEpisodes in each call
for i, call in enumerate(push_calls):
    if 'totalEpisodes' in call:
        print(f"Found totalEpisodes in call #{i}")
        # Find the context
        pos = call.find('totalEpisodes')
        print(f"  Context: {call[pos-20:pos+50]}")
        # Try to extract the number
        match = re.search(r'totalEpisodes["\']?\s*:\s*(\d+)', call)
        if match:
            print(f"  Extracted: {match.group(1)}")
        break