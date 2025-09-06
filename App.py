import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
from io import BytesIO

# ================== FUNCTIONS ==================

def get_data_from_url(url):
    """
    Fetch HTML from the URL and extract:
    - Company pages (aircrafts + engines)
    - Models pages
    - Companies pages (from script or HTML table)
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            scripts = soup.find_all("script")
            extracted_data = {}

            for script_tag in scripts:
                if not script_tag.string:
                    continue
                script_content = script_tag.string

                # 1) Company pages (aircrafts + engines)
                if "var aircrafts" in script_content or "var engines" in script_content:
                    aircrafts_match = re.search(r"var aircrafts = (\[.*?\]);", script_content, re.DOTALL)
                    engines_match = re.search(r"var engines = (\[.*?\]);", script_content, re.DOTALL)

                    if aircrafts_match:
                        aircrafts_json = aircrafts_match.group(1).replace("\u039futright", "Outright")
                        extracted_data["aircrafts"] = json.loads(aircrafts_json)

                    if engines_match:
                        extracted_data["engines"] = json.loads(engines_match.group(1))

                # 2) Listings pages
                if "var listings" in script_content:
                    listings_match = re.search(r"var listings = (\[.*?\]);", script_content, re.DOTALL)
                    if listings_match:
                        extracted_data["listings"] = json.loads(listings_match.group(1))

                # 3) Products pages (inside script)
                if "var products" in script_content:
                    products_match = re.search(r"var products = (\[.*?\]);", script_content, re.DOTALL)
                    if products_match:
                        extracted_data["products"] = json.loads(products_match.group(1))

            # 4) Products from HTML table if no script found
            if "products" not in extracted_data:
                table = soup.find("table", {"id": "myTable"})
                if table:
                    headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
                    rows = []
                    for tr in table.find("tbody").find_all("tr"):
                        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
                        rows.append(cells)
                    if rows:
                        extracted_data["products"] = [dict(zip(headers, row)) for row in rows]

            return extracted_data if extracted_data else None
        else:
            st.error(f"Failed to fetch page. Status code: {response.status_code}")
            return None

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


def process_contcomm_column(df):
    """Extract Name, Email, Phone, and Comments from contcomm column"""
    if df.empty or "contcomm" not in df.columns:
        return df

    email_pattern = r'href="mailto:(.*?)\?subject'
    phone_pattern = r"\+\d{1,4}(?:\s?\d+)*"
    comment_pattern = r"<br>(.*)"
    name_pattern = r'title=".*?">(.*?)<'

    df.columns = df.columns.str.upper()
    
    df["Name"] = df["CONTCOMM"].apply(lambda x: re.search(name_pattern, str(x)).group(1) if re.search(name_pattern, str(x)) else None)
    df["Email"] = df["CONTCOMM"].apply(lambda x: re.search(email_pattern, str(x)).group(1) if re.search(email_pattern, str(x)) else None)
    df["Phone"] = df["CONTCOMM"].apply(lambda x: re.search(phone_pattern, str(x)).group(0) if re.search(phone_pattern, str(x)) else None)
    df["Comments"] = df["CONTCOMM"].apply(lambda x: re.search(comment_pattern, str(x)).group(1) if re.search(comment_pattern, str(x)) else None)

    df.drop(columns=["CONTCOMM"], inplace=True, errors="ignore")
    return df


def to_excel(dfs: dict):
    """Convert multiple DataFrames to a single Excel file in memory"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return output.getvalue()


# ================== STREAMLIT APP ==================

st.set_page_config(page_title="MyAirTrade Data Extractor", page_icon="✈️", layout="wide")

st.title("✈️ MyAirTrade Data Extractor")
st.markdown("Enter a **MyAirTrade URL** to extract aircrafts, engines or Companies data.")

if "data" not in st.session_state:
    st.session_state.data = None

def extract_data():
    url_value = st.session_state.url
    if not url_value.strip():
        st.warning("⚠️ Please enter a valid URL")
        return
    st.session_state.data = get_data_from_url(url_value)

# Input with Enter support
url = st.text_input("Enter the URL:", key="url", on_change=extract_data)

# Optional button
if st.button("Extract Data"):
    extract_data()

# Display results
if st.session_state.data:
    data = st.session_state.data
    dfs = {}

    # Aircrafts
    if "aircrafts" in data:
        aircrafts_df = pd.DataFrame(data.get("aircrafts", []))
        if not aircrafts_df.empty:
            aircrafts_df = aircrafts_df.rename(columns={"hc": "H/C"})
            aircrafts_df = process_contcomm_column(aircrafts_df)
            st.subheader("🛩️ Aircrafts Data")
            st.dataframe(aircrafts_df)
            dfs["Aircrafts"] = aircrafts_df

    # Engines
    if "engines" in data:
        engines_df = pd.DataFrame(data.get("engines", []))
        if not engines_df.empty:
            engines_df.drop(columns=["yom", "hc", "engines", "cc"], inplace=True, errors="ignore")
            engines_df = process_contcomm_column(engines_df)
            st.subheader("🔧 Engines Data")
            st.dataframe(engines_df)
            dfs["Engines"] = engines_df

    # Listings
    if "listings" in data:
        Models_df = pd.DataFrame(data.get("listings", []))
        if not Models_df.empty:
            Models_df.drop(columns=["yom", "hc", "engines", "cc"], inplace=True, errors="ignore")
            Models_df = process_contcomm_column(Models_df)
            st.subheader("📋 Models Data")
            st.dataframe(Models_df)
            dfs["Models"] = Models_df

    # Products
    if "products" in data:
        Companies_df = pd.DataFrame(data.get("products", []))
        if not Companies_df.empty:
            st.subheader("🏭 Companies Data")
            st.dataframe(Companies_df)
            dfs["Companies"] = Companies_df

    # Download Excel
    if dfs:
        excel_bytes = to_excel(dfs)
        st.download_button(
            label="📥 Download Excel File",
            data=excel_bytes,
            file_name="aviation_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



