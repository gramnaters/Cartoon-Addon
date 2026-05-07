import requests, re

r = requests.get('https://animelok.xyz/watch/naruto-20', headers={'User-Agent': 'Mozilla/5.0'})
matches = re.findall(r'"totalEpisodes":\s*(\d+)', r.text)
print(f"Found {len(matches)} matches")
print(matches)