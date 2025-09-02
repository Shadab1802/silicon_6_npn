from app.services.fetcher import download_models
import joblib

paths = download_models()

model=joblib.load(paths["model"])
encoders = joblib.load(paths["encoder"])