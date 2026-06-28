import cv2
import os
import numpy as np
import unicodedata
import logging

class WeaponClassifier:
    def __init__(self, db_path="weapons_db"):
        self.db_path = db_path
        self.orb = cv2.ORB_create()

        self.weapon_features = []

        valid_exts = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}

        for filename in os.listdir(db_path):
            name_norm = unicodedata.normalize('NFC', filename)
            ext = os.path.splitext(name_norm)[1].lower()
            if ext not in valid_exts:
                continue

            weapon_name = os.path.splitext(name_norm)[0]
            path = os.path.join(db_path, filename)

            try:
                with open(path, 'rb') as f:
                    data = f.read()

                nparr = np.frombuffer(data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    logging.warning(f"Unable to decode image: {path}")
                    continue

                kp, des = self.orb.detectAndCompute(img, None)
                if des is None:
                    continue

                self.weapon_features.append((weapon_name, kp, des))
            except Exception as e:
                logging.warning(f"Error loading {path}: {e}")
                continue

    def predict(self, image_bytes: bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return {"weapon_name": None, "score": 0}

        kp1, des1 = self.orb.detectAndCompute(img, None)
        if des1 is None:
            return {"weapon_name": None, "score": 0}

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        best_match = None
        best_score = 0

        for weapon_name, kp2, des2 in self.weapon_features:
            matches = bf.match(des1, des2)
            score = len(matches)

            if score > best_score:
                best_score = score
                best_match = weapon_name

        return {
            "weapon_name": best_match,
            "score": best_score
        }
