#!/usr/bin/env python3
import os
import sys
import unicodedata
import csv
import re
from pathlib import Path

INVALID_CHARS = r'[<>:"/\\|?*]'
TRAILING_DOTS_SPACES = r'[\.\s]+$'

ALLOWED_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}

def sanitize(st: str) -> str:
    # Normalize to NFC
    s = unicodedata.normalize('NFC', st)
    # Remove invalid characters
    s = re.sub(INVALID_CHARS, '_', s)
    # Strip leading/trailing whitespace and dots
    s = re.sub(TRAILING_DOTS_SPACES, '', s)
    # Collapse runs of spaces
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def normalize_db(db_path: str):
    p = Path(db_path)
    if not p.exists():
        print(f"Path not found: {db_path}")
        return

    mapping = []
    total = 0
    renamed = 0
    skipped = 0
    log_lines = []

    for f in sorted(p.iterdir()):
        if not f.is_file():
            continue
        total += 1
        old_name = f.name
        stem, ext = os.path.splitext(old_name)
        ext_l = ext.lower()
        if ext_l not in ALLOWED_EXTS:
            skipped += 1
            continue

        new_stem = sanitize(stem)
        # ensure extension lower-case and normalized
        new_name = new_stem + ext_l

        # Normalize unicode to NFC for filename bytes
        new_name = unicodedata.normalize('NFC', new_name)

        if new_name == old_name:
            mapping.append((old_name, new_name))
            continue

        target = p / new_name
        counter = 1
        while target.exists():
            # avoid overwriting: append suffix
            target = p / f"{new_stem}_{counter}{ext_l}"
            counter += 1

        try:
            f.rename(target)
            mapping.append((old_name, target.name))
            renamed += 1
            log_lines.append(f"Renamed: {old_name} -> {target.name}")
        except Exception as e:
            log_lines.append(f"Failed to rename {old_name}: {e}")
            mapping.append((old_name, old_name))

    # write mapping csv
    csv_path = p / 'rename_map.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['old_name','new_name'])
        for old, new in mapping:
            writer.writerow([old, new])

    # write log file with UTF-8 encoding to avoid console encoding issues
    log_path = p / 'normalize_log.txt'
    with open(log_path, 'w', encoding='utf-8') as lf:
        for L in log_lines:
            lf.write(L + '\n')

    print(f"Total files scanned: {total}")
    print(f"Renamed: {renamed}")
    print(f"Skipped (ext not allowed): {skipped}")
    print(f"Mapping saved to: {csv_path}")
    print(f"Detailed log: {log_path}")


if __name__ == '__main__':
    db = sys.argv[1] if len(sys.argv) > 1 else 'local/weapons_db'
    normalize_db(db)
