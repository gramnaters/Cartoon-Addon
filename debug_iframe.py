import requests, re

url = 'https://toonstream.vip/episode/dr-stone-1x1/'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# Find iframes with full URLs
iframes = re.findall(r'<iframe[^>]*src="([^"]+)"', r.text, re.I)
print(f'Found {len(iframes)} iframes:')
for i in iframes:
    print(f'  {i}')

# Find relative iframes with trembed
rel = re.findall(r'<iframe[^>]*src="([^"]*trembed[^"]*)"', r.text, re.I)
print(f'Relative with trembed: {rel}')