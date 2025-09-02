import requests
import os
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")  

def fetch_prediction(payload: dict):
    """Send request to backend and return prediction result safely."""
    try:
        response = requests.post(f"{BACKEND_URL}/api/predict", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result.get("Delayed", None), result
    except requests.exceptions.RequestException as e:
        st.error(f"Prediction request failed: {e}")
        return None, None