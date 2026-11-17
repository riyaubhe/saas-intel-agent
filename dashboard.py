import streamlit as st
import pandas as pd

st.title("SaaS Hiring & Layoff Signal Tracker")
st.write("Tracking hiring and layoff signals in the SaaS industry, pulled from Hacker News and analyzed with an LLM.")

try:
    signals = pd.read_csv("trends_log.csv")
except FileNotFoundError:
    st.warning("No data yet — run save_trends.py first to collect some signals.")
    st.stop()

st.subheader("All signals collected so far")
st.dataframe(signals)

st.subheader("Hiring vs Layoff breakdown")
type_counts = signals["signal_type"].value_counts()
st.bar_chart(type_counts)

st.subheader("Signals by company")
company_counts = signals["company"].value_counts()
st.bar_chart(company_counts)

if st.button("Fetch new signals now"):
    from save_trends import save_signals
    with st.spinner("Fetching headlines and analyzing..."):
        save_signals()
    st.success("Done! Refresh the page to see updated data.")
