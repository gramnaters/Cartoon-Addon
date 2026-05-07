import requests, re

def check_server(server_num):
    url = f'https://toonstream.vip/?trembed={server_num}&trid=26009&trtype=2'
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://toonstream.vip/episode/dr-stone-1x1/'
    }
    r = requests.get(url, headers=headers)
    iframes = re.findall(r'<iframe[^>]*src="([^"]+)"', r.text, re.I)
    print(f"Server {server_num}: {r.status_code}, {len(iframes)} iframes")
    for i in iframes:
        print(f"  -> {i}")

if __name__ == "__main__":
    for i in range(0, 4):
        check_server(i)