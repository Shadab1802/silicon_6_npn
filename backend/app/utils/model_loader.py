# backend/app/utils/model_loader.py
"""
    It loads the local disk stored file to Program memory at runtime , so that inference can be draw fast
"""

import joblib

model = joblib.load("/app/models/model.pkl")
encoders = joblib.load("/app/models/encoder.pkl")
