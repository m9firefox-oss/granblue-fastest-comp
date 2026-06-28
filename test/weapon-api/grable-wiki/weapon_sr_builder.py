import requests
from bs4 import BeautifulSoup
import json

URL = "https://gbf-wiki.com/?武器SR"
headers = {"User-Agent": "Mozilla/5.0"}

html = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

sr_weapons = {}

# SR は武器種ごとに複数テーブルがある
for table in soup.find_all("table"):
    rows = table.find_all("tr")
    if not rows:
        continue

    header_cols = rows[0].find_all(["th", "td"])
    header_text = [col.get_text(strip=True).replace("\n", " ").strip() for col in header_cols]

    if not any("名前" in text for text in header_text):
        continue
    if not any("属性" in text for text in header_text):
        continue
    if not any("武器種" in text for text in header_text):
        continue

    def find_idx(keys):
        for key in keys:
            for idx, text in enumerate(header_text):
                if key in text:
                    return idx
        return None

    name_idx = find_idx(["名前"])
    element_idx = find_idx(["属性"])
    weapon_type_idx = find_idx(["武器種"])
    rank_idx = find_idx(["適正", "Rank"])
    ougi_idx = find_idx(["奥義"])
    skill1_idx = find_idx(["第1スキル", "スキル1", "スキル"])
    skill2_idx = find_idx(["第2スキル", "スキル2"])
    min_hp_idx = find_idx(["Min HP", "HP"])
    min_atk_idx = find_idx(["Min ATK", "ATK"])
    max_hp_idx = find_idx(["Max HP"])
    max_atk_idx = find_idx(["Max ATK"])

    if name_idx is None or element_idx is None or weapon_type_idx is None:
        continue

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) <= name_idx:
            continue

        name_cell = cols[name_idx]
        name_tag = name_cell.find("a")
        name = (name_tag.text.strip() if name_tag else name_cell.get_text(strip=True))
        if not name:
            continue

        def get_text(idx):
            return cols[idx].get_text(strip=True) if idx is not None and idx < len(cols) else ""

        element = get_text(element_idx)
        weapon_type = get_text(weapon_type_idx)
        rank = get_text(rank_idx)
        ougi = get_text(ougi_idx)
        skill1 = get_text(skill1_idx)
        skill2 = get_text(skill2_idx)
        min_hp = get_text(min_hp_idx)
        min_atk = get_text(min_atk_idx)
        max_hp = get_text(max_hp_idx)
        max_atk = get_text(max_atk_idx)

        sr_weapons[name] = {
            "rarity": "SR",
            "element": element,
            "weapon_type": weapon_type,
            "rank": rank,
            "ougi": ougi,
            "skill1": skill1,
            "skill2": skill2,
            "min_hp": min_hp,
            "min_atk": min_atk,
            "max_hp": max_hp,
            "max_atk": max_atk
        }

with open("weapon_sr.json", "w", encoding="utf-8") as f:
    json.dump(sr_weapons, f, ensure_ascii=False, indent=2)

print("完了！SR武器数:", len(sr_weapons))
