import requests
import os
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")  

def fetch_alternative_flights(origin: str, destination: str):
    """Fetch alternative available flights when the flight is delayed."""
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/alternative",
            params={"origin": origin, "destination": destination},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Alternative flights request failed: {e}")
        return []