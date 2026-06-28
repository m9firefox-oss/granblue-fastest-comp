import sys
import os
import unicodedata
import runpy

sys.path.append(os.getcwd())

from app.domain.weapon_classifier import WeaponClassifier


def find_image(db_path: str, preferred: str = 'ロムフェーヤ') -> str | None:
    # try exact
    exact = os.path.join(db_path, f"{preferred}.png")
    if os.path.exists(exact):
        return exact

    # search normalized filenames for the base name
    base = unicodedata.normalize('NFC', preferred)
    for f in sorted(os.listdir(db_path)):
        if base in unicodedata.normalize('NFC', f):
            return os.path.join(db_path, f)

    # fallback: first allowed image
    allowed = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
    for f in sorted(os.listdir(db_path)):
        if os.path.splitext(f)[1].lower() in allowed:
            return os.path.join(db_path, f)

    return None


def main():
    db = 'local/weapons_db'
    img_path = find_image(db)
    if not img_path:
        print('No image found in', db)
        return

    with open(img_path, 'rb') as fh:
        image_bytes = fh.read()

    clf = WeaponClassifier(db_path=db)
    res = clf.predict(image_bytes)

    # attempt to print human-readable file path and weapon name;
    # fall back to escaped forms if the console encoding can't handle them
    weapon = res.get('weapon_name')
    escaped = weapon.encode('unicode_escape').decode('ascii') if weapon is not None else None
    try:
        print('using_file:', img_path)
    except UnicodeEncodeError:
        print('using_file (escaped):', img_path.encode('unicode_escape').decode('ascii'))

    try:
        print('判定結果:', weapon)
    except UnicodeEncodeError:
        print('判定結果 (escaped):', escaped)

    print('一致スコア:', res.get('score'))


if __name__ == '__main__':
    main()

