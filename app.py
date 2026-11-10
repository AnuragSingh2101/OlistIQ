import streamlit as st

st.title("OlistIQ Demo")
st.write("Welcome to the OlistIQ demo dashboard.")

# Placeholder for your actual analysis logic.
# For example, if you have a function `run_analysis()` in `src/load_data.py`, you could:
# from src.load_data import run_analysis
# result = run_analysis()
# st.write(result)

st.sidebar.header("Controls")
st.sidebar.checkbox("Show raw data", value=False)
# Add more interactive widgets as needed.

