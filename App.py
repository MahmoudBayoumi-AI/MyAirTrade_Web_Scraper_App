import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
from io import BytesIO

# ===== Functions (get_data_from_url, process_contcomm_column, to_excel) =====
# (نفس اللي عندك، مش هكرره كله عشان التركيز على التعديل)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="MyAirTrade Data Extractor", page_icon="✈️", layout="wide")

st.title("✈️ MyAirTrade Data Extractor")
st.markdown("Enter a **MyAirTrade URL** to extract aircrafts, engines, or listings data.")

# مكان نخزن فيه النتيجة (عشان تشتغل سواء Enter أو الزر)
if "data" not in st.session_state:
    st.session_state.data = None

def extract_data():
    url_value = st.session_state.url
    if not url_value.strip():
        st.warning("⚠️ Please enter a valid URL")
        return
    st.session_state.data = get_data_from_url(url_value)

# النص يشتغل Enter = تشغيل الكود
url = st.text_input("Enter the URL:", key="url", on_change=extract_data)

# أو ممكن بالزر
if st.button("Extract Data"):
    extract_data()

# عرض النتائج لو موجودة
if st.session_state.data:
    data = st.session_state.data
    dfs = {}

    if "aircrafts" in data:
        aircrafts_df = pd.DataFrame(data.get("aircrafts", []))
        if not aircrafts_df.empty:
            aircrafts_df = aircrafts_df.rename(columns={"hc": "H/C"})
            aircrafts_df = process_contcomm_column(aircrafts_df)
            st.subheader("📋 Aircrafts Data")
            st.dataframe(aircrafts_df)
            dfs["Aircrafts"] = aircrafts_df

    if "engines" in data:
        engines_df = pd.DataFrame(data.get("engines", []))
        if not engines_df.empty:
            engines_df.drop(columns=["yom", "hc", "engines", "cc"], inplace=True, errors="ignore")
            engines_df = process_contcomm_column(engines_df)
            st.subheader("📋 Engines Data")
            st.dataframe(engines_df)
            dfs["Engines"] = engines_df

    if "listings" in data:
        listings_df = pd.DataFrame(data.get("listings", []))
        if not listings_df.empty:
            listings_df.drop(columns=["yom", "hc", "engines", "cc"], inplace=True, errors="ignore")
            listings_df = process_contcomm_column(listings_df)
            st.subheader("📋 Listings Data")
            st.dataframe(listings_df)
            dfs["Listings"] = listings_df

    if dfs:
        excel_bytes = to_excel(dfs)
        st.download_button(
            label="📥 Download Excel File",
            data=excel_bytes,
            file_name="aviation_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
