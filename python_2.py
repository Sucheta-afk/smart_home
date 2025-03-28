import streamlit as st
from pymongo import MongoClient
import pandas as pd
import time

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["sensor_database"]
collection = db["temperature_humidity"]

# Hardcoded extreme thresholds
TEMP_THRESHOLD = 35  # °C (High)
TEMP_LOW = 15  # °C (Low)
HUMIDITY_THRESHOLD = 70  # % (High)
HUMIDITY_LOW = 30  # % (Low)

st.set_page_config(page_title="🐾 Pet Comfort & Security Monitor", layout="wide")

# Sidebar for Pet Inputs
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🐾 Pet Settings</h2>", unsafe_allow_html=True)
    pet_name = st.text_input("Enter your pet’s name", "Buddy")
    pet_type = st.selectbox("Select Pet Type", ["Dog", "Cat", "Rabbit", "Other"])
    pet_emoji = "🐶" if pet_type == "Dog" else "🐱" if pet_type == "Cat" else "🐰" if pet_type == "Rabbit" else "🐾"

# Page Title
st.markdown(f"<h1 style='text-align: center;'>{pet_emoji} {pet_name}'s Comfort & Security Monitor</h1>", unsafe_allow_html=True)

# Function to fetch latest data
def fetch_latest_data():
    data = list(collection.find().sort("_id", -1).limit(10))
    if not data:
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity", "motion"])
    df = pd.DataFrame(data)
    df = df[["timestamp", "temperature", "humidity", "motion"]]
    return df

# Real-time Dashboard
while True:
    df = fetch_latest_data()

    if not df.empty:
        latest_temp = df.iloc[0]["temperature"]
        latest_humidity = df.iloc[0]["humidity"]
        latest_motion = df.iloc[0]["motion"]

        # Determine Comfort Status
        comfort_message = "😊 Comfortable"
        alert_color = "green"

        if latest_temp > TEMP_THRESHOLD:
            comfort_message = "🥵 Too Hot! Adjust Cooling!"
            alert_color = "red"
        elif latest_temp < TEMP_LOW:
            comfort_message = "🥶 Too Cold! Adjust Heating!"
            alert_color = "blue"

        if latest_humidity > HUMIDITY_THRESHOLD:
            comfort_message = "💦 Too Humid! Ensure Ventilation!"
            alert_color = "orange"
        elif latest_humidity < HUMIDITY_LOW:
            comfort_message = "🌵 Too Dry! Consider a Humidifier!"
            alert_color = "orange"

        # Motion Sensor Alert
        motion_alert = ""
        if latest_motion == 0:
            motion_alert = f"<h2 style='color: red; text-align: center;'>🚨 Intruder Detected at {df.iloc[0]['timestamp']}!</h2>"

        # Compact Row Layout for Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric(label="🌡️ Temperature", value=f"{latest_temp}°C")
        col2.metric(label="💧 Humidity", value=f"{latest_humidity}%")
        col3.markdown(f"<h3 style='color: {alert_color}; text-align: center;'>{comfort_message}</h3>", unsafe_allow_html=True)

        # Motion Alert
        if motion_alert:
            st.markdown(motion_alert, unsafe_allow_html=True)

        # Real-time Graph
        st.subheader("📈 Home Temperature & Humidity Trends")
        st.line_chart(df.set_index("timestamp")[["temperature", "humidity"]])

        # Table for the Last 10 Readings
        st.subheader("📋 Last 10 Sensor Readings")
        st.write(df)

    time.sleep(2)
    st.experimental_rerun()
