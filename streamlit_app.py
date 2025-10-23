# streamlit_app.py
import streamlit as st
import pandas as pd
import random
from db import init_db, insert_data, fetch_recent
from groq_agent import ask_groq, evaluate_safety

# Initialize database
init_db()

# Streamlit page configuration
st.set_page_config(page_title="AquaTrack", page_icon="🐟", layout="centered")
st.title("🐟 AquaTrack: Fish Pond Monitoring")
st.write("Simulate pond water quality, check fish safety, and ask AI questions about the pond.")

# -------------------------
# Step 1: Generate simulated sensor data
# -------------------------
st.subheader("Simulate Sensor Data")
num_samples = st.slider("Number of simulated readings", 1, 50, 5)

if st.button("Generate & Insert Fake Data"):
    new_data = []
    for _ in range(num_samples):
        temp = round(random.uniform(18, 35), 2)  # Temperature in °C
        ph = round(random.uniform(5.5, 9), 2)    # pH
        do = round(random.uniform(3, 10), 2)     # Dissolved Oxygen mg/L
        insert_data(temp, ph, do)
        new_data.append({"Temperature": temp, "pH": ph, "Dissolved Oxygen": do})
    
    st.success(f"{num_samples} new readings added to the database!")
    st.dataframe(pd.DataFrame(new_data))

# -------------------------
# Step 2: Show recent sensor data
# -------------------------
st.subheader("Recent Sensor Data")
recent_df = fetch_recent(limit=50)
if recent_df.empty:
    st.write("No sensor data available.")
else:
    st.dataframe(recent_df[["timestamp", "temperature", "ph", "dissolved_oxygen"]])

# -------------------------
# Step 3: Evaluate water safety
# -------------------------
st.subheader("Water Safety Evaluation")
if not recent_df.empty:
    latest = recent_df.iloc[0]
    status = evaluate_safety(latest['temperature'], latest['ph'], latest['dissolved_oxygen'])
    
    if status == "SAFE":
        st.success("✅ Water conditions are SAFE for fish.")
    else:
        st.error("⚠️ Water conditions are UNSAFE for fish!")
        st.warning("Take immediate action: check aeration, pH, and temperature.")

# -------------------------
# Step 4: Ask AI questions
# -------------------------
st.subheader("Ask AquaTrack AI")
user_question = st.text_input("Enter your question about the pond:")

if st.button("Get AI Answer") and user_question:
    with st.spinner("Generating answer..."):
        answer = ask_groq(user_question)
        st.write(answer)

# -------------------------
# Optional: Charts for visualization
# -------------------------
st.subheader("Sensor Data Trends")
if not recent_df.empty:
    chart_df = recent_df[['timestamp', 'temperature', 'ph', 'dissolved_oxygen']].copy()
    chart_df['timestamp'] = pd.to_datetime(chart_df['timestamp'])
    chart_df.set_index('timestamp', inplace=True)
    
    st.line_chart(chart_df)