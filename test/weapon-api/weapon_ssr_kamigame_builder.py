import json
import re

import requests
from bs4 import BeautifulSoup

URL = "https://kamigame.jp/%E3%82%B0%E3%83%A9%E3%83%96%E3%83%AB/%E6%AD%A6%E5%99%A8/SSR/index.html"
BASE_URL = "https://kamigame.jp"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def parse_detail_cell(td):
    details = {}
    current_label = None

    for child in td.children:
        if getattr(child, "name", None) == "span" and "label" in child.get("class", []):
            current_label = child.get_text(strip=True)
            details[current_label] = ""
            continue

        if current_label is None:
            continue

        if getattr(child, "name", None) == "br":
            continue

        text = child.get_text(" ", strip=True) if getattr(child, "get_text", None) else str(child).strip()
        if not text:
            continue

        if details[current_label]:
            details[current_label] += " " + text
        else:
            details[current_label] = text

    return details


def parse_section_heading(text):
    match = re.match(r"(.+?)属性SSR(.+)", text)
    if not match:
        return None, None
    return match.group(1), match.group(2)


def build_weapon_data():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    weapons = {}

    for heading in soup.find_all("h2"):
        title = heading.get_text(strip=True)
        element, weapon_type = parse_section_heading(title)
        if not element or not weapon_type:
            continue

        table = heading.find_next_sibling("table")
        if not table or "filter-table" not in (table.get("class") or []):
            continue

        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 2:
                continue

            link_tag = cols[0].find("a")
            if not link_tag:
                continue

            name = link_tag.get_text(strip=True)
            detail_url = BASE_URL + link_tag.get("href", "")
            details = parse_detail_cell(cols[1])

            weapons[name] = {
                "rarity": "SSR",
                "element": element,
                "weapon_type": weapon_type,
                "detail_url": detail_url,
                "ougi": details.get("奥義", ""),
                "skill1": details.get("スキル1", ""),
                "skill2": details.get("スキル2", ""),
                "skill3": details.get("スキル3", ""),
            }

    return weapons


if __name__ == "__main__":
    weapon_data = build_weapon_data()

    with open("weapon_ssr_kamigame.json", "w", encoding="utf-8") as f:
        json.dump(weapon_data, f, ensure_ascii=False, indent=2)

    print("完了！SSR武器数:", len(weapon_data))
