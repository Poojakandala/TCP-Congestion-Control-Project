import streamlit as st
import pandas as pd
import joblib

# Load your trained model
model = joblib.load('decision_tree_model.pkl')

st.title("TCP Congestion Prediction")

uploaded_file = st.file_uploader("Upload TCP data (CSV)", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Input data:", data)
    # Drop label column if present
    if 'Actual' in data.columns:
        X = data.drop('Actual', axis=1)
    else:
        X = data
    predictions = model.predict(X)
    st.write("Predicted Congestion States:", predictions)
