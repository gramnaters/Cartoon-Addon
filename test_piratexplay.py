import requests
r = requests.get('https://piratexplay.cc', headers={'User-Agent': 'Mozilla/5.0'})
print(f"PirateXPlay status: {r.status_code}")
if '<title>' in r.text:
    title = r.text.split('<title>')[1].split('</title>')[0]
    print(f"Title: {title}")