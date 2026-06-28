import argparse
import logging
import os
import re
import time
import unicodedata
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


URL = (
    "https://kamigame.jp/%E3%82%B0%E3%83%A9%E3%83%96%E3%83%AB/%E6%AD%A6%E5%99%A8/SSR/index.html"
)


def sanitize_filename(name: str) -> str:
    name = unicodedata.normalize("NFKD", name)
    # remove illegal path chars
    name = re.sub(r"[\\/:*?\"<>|]+", "", name)
    name = name.strip()
    return name[:200]


def get_session(retries: int = 3, backoff: float = 0.3) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; scraper/1.0)"})
    retry = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "POST"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def download_images(output_dir: Path, url: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    session = get_session()

    resp = session.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # The site lists weapons in tables within the main article. Find images inside
    # the article and filter by the site's image host.
    article = soup.find("article") or soup
    imgs = article.find_all("img", src=True)
    logging.info("Found %d img tags in article", len(imgs))

    for img_tag in imgs:
        img_url = img_tag.get("src")
        if not img_url:
            continue
        # prefer kamigame's image host to avoid icons and UI images
        if "img.kamigame.jp" not in img_url:
            continue

        if img_url.startswith("//"):
            img_url = "https:" + img_url
        elif img_url.startswith("/"):
            img_url = "https://kamigame.jp" + img_url

        weapon_name = img_tag.get("alt") or img_tag.get("title") or ""
        weapon_name = weapon_name.strip()
        if not weapon_name:
            # fallback: try text in nearest parent link
            parent_a = img_tag.find_parent("a")
            if parent_a and parent_a.get("href"):
                weapon_name = Path(parent_a.get("href")).stem

        if not weapon_name:
            weapon_name = Path(img_url).stem

        safe_name = sanitize_filename(weapon_name)

        try:
            r = session.get(img_url, stream=True, timeout=20)
            r.raise_for_status()
        except Exception as e:
            logging.warning("Failed to download %s (%s): %s", weapon_name, img_url, e)
            continue

        content_type = r.headers.get("Content-Type", "")
        if "png" in content_type:
            ext = ".png"
        elif "webp" in content_type:
            ext = ".webp"
        elif "jpeg" in content_type or "jpg" in content_type:
            ext = ".jpg"
        else:
            ext = Path(img_url).suffix or ".img"

        save_path = output_dir / f"{safe_name}{ext}"
        if save_path.exists():
            logging.info("Skipping existing: %s", save_path.name)
            continue

        try:
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            logging.info("Downloaded: %s -> %s", weapon_name, save_path.name)
            time.sleep(0.1)
        except Exception as e:
            logging.error("Error saving %s: %s", save_path, e)


def main():
    parser = argparse.ArgumentParser(description="Scrape kamigame SSR weapon images")
    parser.add_argument("--output", "-o", default="weapons_db", help="Output directory")
    parser.add_argument("--url", default=URL, help="Page URL to scrape")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    base = Path(__file__).parent
    outdir = (base / args.output).resolve()
    download_images(outdir, args.url)


if __name__ == "__main__":
    main()
