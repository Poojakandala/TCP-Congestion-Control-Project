import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interactive TCP Data Plotter")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your TCP CSV data", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Dataset preview:", data.head())

    # Select variables
    x_var = st.selectbox("X Variable:", data.columns)
    y_var = st.selectbox("Y Variable:", data.columns)
    plot_type = st.selectbox("Plot Type:", ["Scatterplot", "Lineplot"])

    color_var = "congestion" if "congestion" in data.columns else None

    # Plot
    if plot_type == "Scatterplot":
        fig = px.scatter(data, x=x_var, y=y_var, color=color_var,
                         title=f"{y_var} vs {x_var}")
    else:
        fig = px.line(data, x=x_var, y=y_var, color=color_var,
                      title=f"{y_var} vs {x_var}")

    st.plotly_chart(fig, use_container_width=True)

    # Example: Mean time calculation
    if "resend_time" in data.columns:
        mean_resend = data["resend_time"].mean()
        st.markdown(f"**Mean Time Taken to Resend After Congestion (ms):** {mean_resend:.2f}")
