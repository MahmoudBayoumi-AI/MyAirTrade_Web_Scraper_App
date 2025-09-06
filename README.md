# ✈️ MyAirTrade Data Extractor

A simple **Streamlit web app** that extracts **Aircrafts, Engines, and Companies (Products)** data from [MyAirTrade](https://www.myairtrade.com/) pages and exports them into an Excel file.

---

## 🚀 Features
- Extracts data from multiple MyAirTrade page types:
  - **Aircrafts**  
  - **Engines**  
  - **Companies / Products**
- Cleans and processes contact information:
  - Name  
  - Email  
  - Phone  
  - Comments
- Displays the extracted data in interactive tables inside the web app.
- Allows direct **Excel file download** with multiple sheets:
  - `Aircrafts`  
  - `Engines`  
  - `Companies`

---

## 🛠️ Technologies Used
- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [OpenPyXL](https://openpyxl.readthedocs.io/)
- [Regex](https://docs.python.org/3/library/re.html)
- [Requests](https://docs.python-requests.org/)

---


## 📦 Installation (Run Locally)

1. Clone this repository:
   ```bash
   git clone https://github.com/MahmoudBayoumi-AI/MyAirTrade_Web_Scraper_App.git
   cd myairtrade-extractor
2.Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
```
3.Install dependencies:
   ```bash
pip install -r requirements.txt
   ```
4.Run the Streamlit app:
   ```bash
streamlit run app.py
   ```

## 📖 Example Usage

**Example MyAirTrade company URL:**
```arduine
https://www.myairtrade.com/companies/acc_aviation_group?utm_source=chatgpt.com
```

**The app will fetch and display:**
- **Aircrafts Table** → shows aircraft details such as type, model, year, and contact info.  
- **Engines Table** → shows engine details such as type, status, and contact info.
- Companies Table (Products) → shows available products/companies and details.

**Excel file output:**
- `Aircrafts` sheet → contains all extracted aircrafts data.  
- `Engines` sheet → contains all extracted engines data.  
- `Companies` sheet → contains all extracted products/companies data.
---

## 🌐 Deployment

You can deploy this app easily using [Streamlit Cloud](https://streamlit.io/cloud).  
After pushing the repository to GitHub:

1. Go to **Streamlit Cloud**.  
2. Connect your GitHub repository.  
3. Select `App.py` as the entry point.  
4. Deploy and share the link with others.  

---

