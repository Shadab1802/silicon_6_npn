import streamlit as st
import pandas as pd
from datetime import date, datetime
import numpy as np
import os
import plotly.express as px
import requests   # For FAST API backend integration
import json
from input_model import Input
from backendReq.fetch_flights import fetch_alternative_flights
from backendReq.fetch_prediction import fetch_prediction

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")  # This BACKEND_URL if found in EC2 instance .env file then it will send request to that file only
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # we do store some of files in frontend, to make user expeience smooth and understanding
# like states name is shown instead of code - much user convenient

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
    st.image("airplane.png", width=80)
with col_title:
    st.markdown("<span class='header'>🚦 Flight Delay Prediction Center</span>", unsafe_allow_html=True)
    st.caption("Real-time, AI-driven flight delay analytics. Upload flights, get predictions, and visualize results all in one platform.")

# ---- Sidebar for User Theme and Settings ----
with st.sidebar:
    st.header("🖌️ Appearance & Settings")
    theme = st.radio("Theme:", options=["Light", "Dark"], index=0)
    st.write("[Support](mailto:shekharsingh824101@gmail.com)")
    st.divider()
    st.header("🛠️ Advanced Analysis")
    st.checkbox("Enable real-time weather API (simulated)")
    st.divider()
    st.caption("All predictions are powered by live data & AI algorithms.")

# ---- Tabs for Single and Batch Predictions ----
tab1, tab2 = st.tabs(["🔍User", "📂 Airlies (CSV)"])

#  for single user .i.e. use have to give inputs to fields
 
with tab1:
    st.subheader("Predict Delay for a Single Flight")
    with st.form("flight_form"):
        flight_date = st.date_input("FLIGHT DATE",min_value=date.today())    # for individual user only future dates enter is allowded  
        
        # API Responce for dynamic airline select 
        # response = requests.get(f"{BACKEND_URL}/api/airlines")
        json_path = os.path.join(BASE_DIR, "airlines.json")
        with open(json_path, "r") as f:
            airlines_dict = json.load(f)

        # user see airlines name but input field get code as input
        airline = st.selectbox(
            "AIRLINE",
            options=list(airlines_dict.keys()),
            format_func=lambda x: airlines_dict[x]
        )

         #API responce for dynamic state select
        # response = requests.get(f'{BACKEND_URL}/api/states')\
        json_path = os.path.join(BASE_DIR, "states.json")
        with open(json_path, "r") as f:
            states_dict = json.load(f)
        
        origin_state = st.selectbox(
            "ORIGIN STATE",
            options=list(states_dict.keys()),
            format_func=lambda x: states_dict[x]
        )

        destination_state = st.selectbox(
            "DESTINATION STATE",
            options=[s for s in states_dict.keys() if s != origin_state],
            format_func=lambda x: states_dict[x]
        )

        departure_time = st.time_input("DEPARTURE TIME",value=datetime.now()) 
        arrival_time = st.time_input("ARRIVAL TIME",value=datetime.now())

        json_path = os.path.join(BASE_DIR, "avg_dept_delay.json")
        with open(json_path, "r") as f:
            avg_dept_delay = json.load(f)

        # if normal user don't know what's the departure delay of any airline fron frontend the we just feed the avg dept_delay of tha airline to thid field
        departure_delay = st.number_input("DEPARTURE_DELAY (min)", min_value=0.0, max_value=1000.0, value=float(avg_dept_delay[airline]))
       
        tooltip = "Integrates historical and real-time data for best results."
        submit_btn = st.form_submit_button("🚀 Predict Delay", help=tooltip)

    if submit_btn:
        with st.spinner("⏳ Running advanced AI prediction..."):
            
            input_data = Input(
                DATE=flight_date,
                AIRLINE=airline,
                DEPARTURE_TIME=departure_time,
                ARRIVAL_TIME=arrival_time,
                ORIGIN_STATE=origin_state,
                DESTINATION_STATE=destination_state,
                DEPARTURE_DELAY=float(departure_delay)
            )

            payload = input_data.dict()

            """Send request to backend and return prediction result safely."""
            try:

                prediction, full_result = None,None

                if prediction is None:
                    st.warning("Could not get prediction from server.")
                elif prediction == 0:
                    st.success("✅ Your flight is on time!")
                else:
                    st.error("⚠️ Your flight may be delayed.")

                    # Fetch alternative flights
                    with st.spinner("Fetching alternative flights..."):
                        alternatives = fetch_alternative_flights(payload)

                    if alternatives:
                        df = pd.DataFrame(alternatives)
                        st.subheader("Available Alternative Flights")
                        st.table(df)
                    else:
                        st.info("No alternative flights found at the moment.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")



with tab2:
    st.subheader("Predict Delays for Multiple Flights (Upload CSV)")
    st.write("CSV with columns: Flight Number, Airline, Origin, Destination, Departure Date, Departure Time, Arrival Time, Aircraft Type, Weather, Peak Hour, On Holiday")
    uploaded_file = st.file_uploader("Upload Flight CSV", type=["csv"])
    if uploaded_file:
        df_batch = pd.read_csv(uploaded_file)
        with st.spinner("Batch predictions in progress..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                response = requests.post(f"{BACKEND_URL}/api/batch_predict", files=files)

                if response.status_code == 200:
                    result = response.json()

                    # Show as table
                    st.success("All batch predictions complete! Results below ⬇️")
                    df_batch = pd.DataFrame(result)
                    st.dataframe(df_batch)

                    # st.subheader("Flight Delay Overview")
                    # fig = px.pie(df_batch, names='Prediction', title='Delay Breakdown', color='Prediction',
                    #             color_discrete_map={"🟢 On Time":"mediumspringgreen","🔴 Delay Possible":"tomato"})
                    # st.plotly_chart(fig, use_container_width=True)
                    # st.snow()

                    # st.subheader("Confidence Score Distribution")
                    # fig2 = px.histogram(df_batch, x="Confidence", color="Prediction", nbins=10)
                    # st.plotly_chart(fig2, use_container_width=True)

                    csv = df_batch.to_csv(index=False).encode('utf-8')
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
# ---- Footer ----
st.markdown("---")
colA, colB = st.columns([5,6])
with colA:
    st.markdown("Made by SILICON 6❤️")
