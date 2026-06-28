import os
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials

# ====== ここに自分のキーを入れる ======
ENDPOINT = "<your-training-endpoint>"
TRAINING_KEY = "<your-training-key>"
PROJECT_ID = "<your-project-id>"
# ======================================

# Custom Vision クライアント
credentials = ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

# データフォルダ
BASE_DIR = os.path.join(os.path.dirname(__file__), "weapons")

def upload_images():
    print("=== Uploading images ===")

    for weapon_name in os.listdir(BASE_DIR):
        weapon_dir = os.path.join(BASE_DIR, weapon_name)
        if not os.path.isdir(weapon_dir):
            continue

        print(f"Uploading: {weapon_name}")

        # タグを取得 or 作成
        tag = None
        for t in trainer.get_tags(PROJECT_ID):
            if t.name == weapon_name:
                tag = t
                break
        if tag is None:
            tag = trainer.create_tag(PROJECT_ID, weapon_name)

        # 画像をアップロード
        image_entries = []
        for filename in os.listdir(weapon_dir):
            file_path = os.path.join(weapon_dir, filename)
            with open(file_path, "rb") as img:
                image_entries.append(
                    ImageFileCreateEntry(
                        name=filename,
                        contents=img.read(),
                        tag_ids=[tag.id]
                    )
                )

        if image_entries:
            trainer.create_images_from_files(PROJECT_ID, images=image_entries)

def train_model():
    print("=== Training model ===")
    iteration = trainer.train_project(PROJECT_ID)
    iteration = trainer.get_iteration(PROJECT_ID, iteration.id)

    # 公開（publish）
    trainer.update_iteration(PROJECT_ID, iteration.id, is_default=True)
    print(f"Model trained and published: {iteration.id}")

if __name__ == "__main__":
    upload_images()
    train_model()
