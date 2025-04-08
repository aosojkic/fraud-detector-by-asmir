import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Fraud Detection Tool", layout="centered")

st.title("💳 Suspicious Transaction Detector")
st.markdown("A fraud detection tool that flags suspicious banking transactions based on predefined risk rules.")
st.markdown("**By Asmir Osojkic**")
st.markdown("---")
st.markdown("📁 Upload a CSV file of transactions or test the app with built-in sample data.")

uploaded_file = st.file_uploader("Upload Transaction CSV", type=["csv"])

# Load user file or sample data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully.")
else:
    st.info("No file uploaded — using sample transaction data.")
    data = {
        "transaction_id": ["T1", "T2", "T3", "T4"],
        "customer_id": ["C1001", "C1001", "C2002", "C2002"],
        "amount": [15000, 3000, 9500, 300],
        "location": ["Atlanta, GA", "Miami, FL", "Chicago, IL", "Chicago, IL"],
        "time": [
            "2025-04-08 12:01:00",
            "2025-04-08 12:20:00",
            "2025-04-08 13:00:00",
            "2025-04-08 13:03:00"
        ]
    }
    df = pd.DataFrame(data)

# Convert time column to datetime
df['time'] = pd.to_datetime(df['time'])
st.write("🔍 Analyzing the following transactions:")
st.dataframe(df)

# Analyze transactions
flagged = []

for i, row in df.iterrows():
    reasons = []

    if row['amount'] > 10000:
        reasons.append("High-value transaction")

    customer_id = row['customer_id']
    time_window = row['time'] - timedelta(minutes=60)
    recent = df[(df['customer_id'] == customer_id) &
                (df['time'] >= time_window) &
                (df['time'] < row['time'])]

    if len(recent) >= 2:
        reasons.append("Multiple transactions in 1 hour")

    if reasons:
        flagged.append({
            "transaction_id": row['transaction_id'],
            "customer_id": row['customer_id'],
            "amount": row['amount'],
            "time": row['time'],
            "location": row['location'],
            "reasons": ", ".join(reasons)
        })

# Show results
if flagged:
    st.subheader("⚠️ Suspicious Transactions Found")
    flagged_df = pd.DataFrame(flagged)
    st.dataframe(flagged_df)
else:
    st.success("✅ No suspicious transactions detected.")

st.markdown("---")
st.caption("Made with ❤️ by Asmir Osojkic | Spring 2025")
