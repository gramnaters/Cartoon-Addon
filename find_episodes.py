import re

with open('animelok_page.html', 'r', encoding='utf-8') as f:
    text = f.read()
    matches = re.findall(r'.{0,100}episode.{0,100}', text, re.I)
    for m in matches:
        print(f"--- MATCH ---\n{m}\n")
