import streamlit as st
import requests
import pandas as pd
from io import BytesIO
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")  # default local

st.header("Batch Prediction via CSV")
uploaded_file = st.file_uploader("Upload CSV for batch prediction", type=["csv"], key="batch")

if uploaded_file is not None:
    st.write(f"File uploaded: {uploaded_file.name}")
    
    if st.button("Predict Batch"):
        with st.spinner("Sending CSV to backend..."):
            try:
                # Prepare file for request
                files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
                response = requests.post(f"{BACKEND_URL}/api/airlines", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Predictions received!")
                    
                    # Show as table
                    df_result = pd.DataFrame(result)
                    st.dataframe(df_result)
                    
                    # Allow CSV download
                    csv = df_result.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download predictions as CSV",
                        data=csv,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
