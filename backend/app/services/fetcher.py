from app.core.s3 import get_s3_client
import os
from app.core.config import settings

MODEL_DIR = "/app/models"

FILES = {
    "model": ("flight_model.pkl", os.path.join(MODEL_DIR, "model.pkl")),
    "encoder": ("encoders.pkl", os.path.join(MODEL_DIR, "encoder.pkl")),
}

def download_models():
    """Download model & encoder from S3 if not already present"""
    s3 = get_s3_client()
    local_paths = {}

    for key, (s3_path, local_path) in FILES.items():
        if not os.path.exists(local_path):
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3.download_file(settings.bucket_name, s3_path, local_path)
            print(f"✅ {key} downloaded from S3")
        else:
            print(f"✅ {key} already exists locally")
        local_paths[key] = local_path

    return local_paths
