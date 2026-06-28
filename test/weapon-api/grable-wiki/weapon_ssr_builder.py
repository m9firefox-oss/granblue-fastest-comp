import requests
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "Mozilla/5.0"}

# SSR と 特殊SSR のみ
PAGES = {
    "SSR": "https://gbf-wiki.com/?武器SSR",
    "SSR特殊": "https://gbf-wiki.com/?武器SSR/特殊武器"
}

all_weapons = {}

def parse_weapon_table(url, rarity_label):
    print(f"取得中: {rarity_label} {url}")

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue

        header_cols = rows[0].find_all(["th", "td"])
        col_count = len(header_cols)

        # SSR / 特殊SSR の武器テーブルは 15列以上
        if col_count < 12:
            continue

        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) < 12:
                continue

            name_tag = cols[1].find("a")
            if not name_tag:
                continue

            name = name_tag.text.strip()

            element = cols[2].text.strip()
            weapon_type = cols[3].text.strip()
            suitable = cols[4].text.strip()
            ougi = cols[6].text.strip()
            skill1 = cols[7].text.strip()
            skill2 = cols[8].text.strip()
            skill3 = cols[9].text.strip()  # ← 修正：skill3 を保存する
            min_hp = cols[11].text.strip()
            min_atk = cols[12].text.strip()
            max_hp = cols[13].text.strip()
            max_atk = cols[14].text.strip()

            all_weapons[name] = {
                "rarity": rarity_label,
                "element": element,
                "weapon_type": weapon_type,
                "suitable": suitable,
                "ougi": ougi,
                "skill1": skill1,
                "skill2": skill2,
                "skill3": skill3,
                "min_hp": min_hp,
                "min_atk": min_atk,
                "max_hp": max_hp,
                "max_atk": max_atk
            }


# SSR + 特殊SSR を処理
for rarity, url in PAGES.items():
    parse_weapon_table(url, rarity)

# JSON 保存
with open("weapon_ssr.json", "w", encoding="utf-8") as f:
    json.dump(all_weapons, f, ensure_ascii=False, indent=2)

print("完了！SSR + 特殊SSR 武器数:", len(all_weapons))
