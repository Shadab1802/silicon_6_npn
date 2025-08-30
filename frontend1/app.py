import streamlit as st
import pandas as pd
import time
import numpy as np
import plotly.express as px
import requests   # For REST API backend integration

st.set_page_config(
    page_title="Flight Delay Prediction",
    page_icon="🛩️",
    layout="wide"
)

# ---- Custom Theme Styling and Animations ----
st.markdown("""
<style>
@keyframes pulse {
    0%   {color:#2368A2;}
    50%  {color:#DAA520;}
    100% {color:#2368A2;}
}
.header {
    font-size:60px;
    font-weight:bold;
    color:#2368A2;
    animation:pulse 1.5s infinite;
}
.stButton button {
    background-color: #2368A2;
    color:white;
    font-size:18px;
    border-radius:8px;
}
.stFileUploader label {
    font-size:18px;
}
.metric-box {
    background-color:#ecf3fc;
    border-radius:10px;
    padding:15px;
}
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1,6])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e3/Airplane_icon.png", width=80)
with col_title:
    st.markdown("<span class='header'>🚦 Flight Delay Prediction Center</span>", unsafe_allow_html=True)
    st.caption("Real-time, AI-driven flight delay analytics. Upload flights, get predictions, and visualize results all in one platform.")

# ---- Sidebar for User Theme and Settings ----
with st.sidebar:
    st.header("🖌️ Appearance & Settings")
    theme = st.radio("Theme:", options=["Light", "Dark"], index=0)
    st.write("[Support](mailto:shekharsingh824101@gmail.com) | [Source Code](https://github.com/Shadab1802/flight_prediction_npn)")
    st.divider()
    st.header("🛠️ Advanced Analysis")
    st.checkbox("Enable real-time weather API (simulated)")
    st.divider()
    st.caption("All predictions are powered by live data & AI algorithms.")

# ---- Tabs for Single and Batch Predictions ----
tab1, tab2 = st.tabs(["🔍User", "📂 Airlies (CSV)"])

with tab1:
    st.subheader("Predict Delay for a Single Flight")
    with st.form("flight_form"):
        month = st.selectbox("MONTH", 
                             ["January","February","March","April","May","June","July","August","September","October","November","December"])
        day_of_week = st.selectbox("DAY OF WEEK", 
                                   ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        airline = st.selectbox("AIRLINE", ["Delta", "United", "JetBlue", "American", "Southwest", "Other"])
        departure_time = st.time_input("DEPARTURE TIME")
        elapsed_time = st.number_input("ELAPSED TIME (min)", min_value=10, max_value=1000, value=90)
        air_time = st.number_input("AIR TIME (min)", min_value=10, max_value=1000, value=80)
        arrival_time = st.time_input("ARRIVAL TIME")
        origin_state = st.selectbox("ORIGIN STATE", ["CA", "NY", "TX", "FL", "IL", "Other"])
        destination_state = st.selectbox("DESTINATION STATE", ["CA", "NY", "TX", "FL", "IL", "Other"])
        tooltip = "Integrates historical and real-time data for best results."
        submit_btn = st.form_submit_button("🚀 Predict Delay", help=tooltip)

    if submit_btn:
        with st.spinner("⏳ Running advanced AI prediction..."):
            # ----- Replace with your backend prediction endpoint -----
            payload = {
                "month": month,
                "day_of_week": day_of_week,
                "airline": airline,
                "departure_time": str(departure_time),
                "elapsed_time": elapsed_time,
                "air_time": air_time,
                "arrival_time": str(arrival_time),
                "origin_state": origin_state,
                "destination_state": destination_state
            }
            try:
                response = requests.post("http://localhost:8000/predict", json=payload)  # Change URL to your backend
                result = response.json()
                prediction = result.get('prediction', 'Error')
                confidence = result.get('confidence', 0)
            except Exception as e:
                prediction = "Error"
                confidence = 0
        st.success(f"Prediction for {airline}: {prediction}")
        st.metric("Confidence Level", f"{confidence}%", 
                  delta=f"{confidence-70 if prediction=='🟢 On Time' else confidence-60}%")
        st.balloons()
        summary_df = pd.DataFrame({
            "MONTH": [month],
            "DAY_OF_WEEK": [day_of_week],
            "AIRLINE": [airline],
            "DEPARTURE_TIME": [departure_time],
            "ELAPSED_TIME": [elapsed_time],
            "AIR_TIME": [air_time],
            "ARRIVAL_TIME": [arrival_time],
            "ORIGIN_STATE": [origin_state],
            "DESTINATION_STATE": [destination_state],
            "Prediction": [prediction],
            "Confidence": [f"{confidence}%"]
        })
        st.write("Prediction Details:")
        st.dataframe(summary_df)

with tab2:
    st.subheader("Predict Delays for Multiple Flights (Upload CSV)")
    st.write("CSV with columns: Flight Number, Airline, Origin, Destination, Departure Date, Departure Time, Arrival Time, Aircraft Type, Weather, Peak Hour, On Holiday")
    uploaded_file = st.file_uploader("Upload Flight CSV", type=["csv"])
    if uploaded_file:
        df_batch = pd.read_csv(uploaded_file)
        with st.spinner("Batch predictions in progress..."):
            try:
                flights = df_batch.to_dict("records")
                response = requests.post("http://localhost:8000/batch_predict", json={"flights": flights})  # Update URL
                batch_results = response.json()
                df_batch["Prediction"] = [r["prediction"] for r in batch_results]
                df_batch["Confidence"] = [r["confidence"] for r in batch_results]
            except Exception as e:
                df_batch["Prediction"] = ["Error"] * len(df_batch)
                df_batch["Confidence"] = [0] * len(df_batch)
        st.success("All batch predictions complete! Results below ⬇️")
        st.dataframe(df_batch)
        st.subheader("Flight Delay Overview")
        fig = px.pie(df_batch, names='Prediction', title='Delay Breakdown', color='Prediction',
                     color_discrete_map={"🟢 On Time":"mediumspringgreen","🔴 Delay Possible":"tomato"})
        st.plotly_chart(fig, use_container_width=True)
        st.snow()

        st.subheader("Confidence Score Distribution")
        fig2 = px.histogram(df_batch, x="Confidence", color="Prediction", nbins=10)
        st.plotly_chart(fig2, use_container_width=True)

# ---- Footer ----
st.markdown("---")
colA, colB = st.columns([5,6])
with colA:
    st.markdown("Made by SILICON 6❤️")
