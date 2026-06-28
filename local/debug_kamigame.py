import requests
from bs4 import BeautifulSoup

URL = "https://kamigame.jp/%E3%82%B0%E3%83%A9%E3%83%96%E3%83%AB/%E6%AD%A6%E5%99%A8/SSR/index.html"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(URL, headers=headers, timeout=15)
r.raise_for_status()
html = r.text

with open('local/kamigame_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Saved local/kamigame_page.html, length:', len(html))

soup = BeautifulSoup(html, 'html.parser')

candidates = ['.a-list__item', '.a-list__item__title', 'ul.a-list', 'div.card', 'article', 'li']
for sel in candidates:
    found = soup.select(sel)
    print(f"Selector {sel}: found {len(found)}")

# Print a short sample around likely list areas
for ul in soup.find_all('ul')[:3]:
    print('\n--- UL sample ---')
    print(ul.prettify()[:1000])
    break
