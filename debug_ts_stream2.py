import requests, re
from bs4 import BeautifulSoup

url = "https://toonstream.vip/episode/dr-stone-1x1/"
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://toonstream.vip/"}

r = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

# Look for any links with trembed in them
all_links = soup.find_all("a", href=True)
trembed_links = [a for a in all_links if "trembed" in a.get("href", "")]
print(f"Trembed links: {len(trembed_links)}")
for a in trembed_links[:5]:
    print(f"  {a.get('href')}")

# Also check data attributes
data_attrs = soup.find_all(attrs={"data-trembed": True})
print(f"Data-trembed: {len(data_attrs)}")

# Let's look for the structure in the HTML
# Look for iframes
iframes = soup.find_all("iframe")
print(f"\nIframes: {len(iframes)}")
for i in iframes[:3]:
    print(f"  src: {i.get('src')}")

# Check for video player div
player_div = soup.find(class_=re.compile("player|video", re.I))
if player_div:
    print(f"\nPlayer div found")
    # Look for links inside it
    inner_links = player_div.find_all("a", href=True)
    print(f"  Inner links: {len(inner_links)}")
    for a in inner_links[:5]:
        print(f"    {a.get('href')}")