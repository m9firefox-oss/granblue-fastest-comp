# app/infrastructure/customvision_client.py

import requests
from app.config import (
    CUSTOM_VISION_PREDICTION_ENDPOINT,
    CUSTOM_VISION_PREDICTION_KEY,
    CUSTOM_VISION_PUBLISHED_NAME,
)

class CustomVisionClient:
    """
    Azure Custom Vision の Prediction API を扱うクライアント。
    API 側（weapons.py）はこのクラスだけ使えばよい。
    """

    def __init__(self):
        self.endpoint = CUSTOM_VISION_PREDICTION_ENDPOINT
        self.key = CUSTOM_VISION_PREDICTION_KEY
        self.published_name = CUSTOM_VISION_PUBLISHED_NAME

        # Prediction API の URL
        self.url = f"{self.endpoint}/customvision/v3.0/Prediction/{self.published_name}/classify/iterations/{self.published_name}/image"

        self.headers = {
            "Prediction-Key": self.key,
            "Content-Type": "application/octet-stream",
        }

    def predict(self, image_bytes: bytes) -> dict:
        """
        画像バイト列を Custom Vision に送信し、
        推論結果（タグ名と確率）を返す。
        """
        response = requests.post(self.url, headers=self.headers, data=image_bytes)

        if response.status_code != 200:
            raise Exception(f"Prediction API error: {response.status_code}, {response.text}")

        result = response.json()

        # 最も確率が高いタグを返す
        predictions = result.get("predictions", [])
        if not predictions:
            return {"tag": None, "probability": 0.0}

        top = predictions[0]
        return {
            "tag": top["tagName"],
            "probability": top["probability"],
        }
