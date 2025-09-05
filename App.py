import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from io import BytesIO

# ---------------------------------------------------
# Data extraction functions
# ---------------------------------------------------
def get_data_from_url(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            script_tag = soup.find('script', string=re.compile('var engines'))

            if script_tag:
                script_content = script_tag.string

                aircrafts_match = re.search(r'var aircrafts = (\[.*?\]);', script_content, re.DOTALL)
                engines_match = re.search(r'var engines = (\[.*?\]);', script_content, re.DOTALL)

                extracted_data = {}

                if aircrafts_match:
                    aircrafts_json = aircrafts_match.group(1).replace('\u039futright', 'Outright')
                    extracted_data['aircrafts'] = json.loads(aircrafts_json)

                if engines_match:
                    extracted_data['engines'] = json.loads(engines_match.group(1))

                return extracted_data
            else:
                st.error("❌ No data script found in the page.")
                return None
        else:
            st.error(f"❌ Failed to fetch the page. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"⚠️ Error occurred: {e}")
        return None

def process_contcomm_column(df):
    if df.empty or 'contcomm' not in df.columns:
        return pd.DataFrame(columns=['Email', 'Phone', 'Comments', 'Name'])

    email_pattern = r'href="mailto:(.*?)\?subject'
    phone_pattern = r'\+\d{1,4}(?:\s?\d+)*'
    comment_pattern = r'<br>(.*)'
    name_pattern = r'title=".*?">(.*?)<'

    df.columns = df.columns.str.upper()
    df['Name'] = df['CONTCOMM'].apply(lambda x: re.search(name_pattern, str(x)).group(1) if re.search(name_pattern, str(x)) else None)
    df['Email'] = df['CONTCOMM'].apply(lambda x: re.search(email_pattern, str(x)).group(1) if re.search(email_pattern, str(x)) else None)
    df['Phone'] = df['CONTCOMM'].apply(lambda x: re.search(phone_pattern, str(x)).group(0) if re.search(phone_pattern, str(x)) else None)
    df['Comments'] = df['CONTCOMM'].apply(lambda x: re.search(comment_pattern, str(x)).group(1) if re.search(comment_pattern, str(x)) else None)

    return df.drop(columns=['CONTCOMM'])

# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.title("✈️ MyAirTrade Data Extractor")
st.markdown("Enter a company link from **myairtrade.com** to extract aircrafts and engines data into an Excel file.")

url = st.text_input("🔗 Enter company URL:")

if st.button("Extract Data"):
    if url:
        data = get_data_from_url(url)

        if data:
            # Aircrafts
            aircrafts_df = pd.DataFrame(data.get('aircrafts', []))
            if not aircrafts_df.empty:
                aircrafts_df = aircrafts_df.rename(columns={'hc': 'H/C'})
                aircrafts_df = process_contcomm_column(aircrafts_df)
                st.subheader("📋 Aircrafts Data")
                st.dataframe(aircrafts_df)
            else:
                st.info("ℹ️ No aircrafts data found.")

            # Engines
            engines_df = pd.DataFrame(data.get('engines', []))
            if not engines_df.empty:
                engines_df.drop(columns=['yom', 'hc', 'engines', 'cc'], inplace=True, errors="ignore")
                engines_df = process_contcomm_column(engines_df)
                st.subheader("📋 Engines Data")
                st.dataframe(engines_df)
            else:
                st.info("ℹ️ No engines data found.")

            # Export to Excel
            if not aircrafts_df.empty or not engines_df.empty:
                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    aircrafts_df.to_excel(writer, sheet_name="Aircrafts", index=False)
                    engines_df.to_excel(writer, sheet_name="Engines", index=False)
                excel_data = output.getvalue()

                st.download_button(
                    label="📥 Download Excel file",
                    data=excel_data,
                    file_name="aviation_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.warning("⚠️ Please enter a valid URL.")
