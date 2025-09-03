import joblib

model = joblib.load("app/models/model.pkl")
encoders = joblib.load("app/models/encoder.pkl")