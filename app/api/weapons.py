# app/api/weapons.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.domain.weapon_classifier import WeaponClassifier

router = APIRouter()
classifier = WeaponClassifier()

@router.post("/predict")
async def predict_weapon(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="画像ファイルをアップロードしてください。")

    image_bytes = await file.read()
    result = classifier.predict(image_bytes)
    return result
