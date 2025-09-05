# ✈️ MyAirTrade Data Extractor

A simple **Streamlit web app** that extracts **aircrafts** and **engines** data from [MyAirTrade](https://www.myairtrade.com/) company pages and exports them into an Excel file.

---

## 🚀 Features
- Extracts **aircrafts** and **engines** data from any MyAirTrade company page.
- Cleans and processes contact information:
  - Name
  - Email
  - Phone
  - Comments
- Displays the extracted data in interactive tables inside the web app.
- Allows direct **Excel file download** with two sheets:
  - `Aircrafts`
  - `Engines`

---

## 🛠️ Technologies Used
- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [OpenPyXL](https://openpyxl.readthedocs.io/)

---

## 📦 Installation (Run Locally)

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/myairtrade-extractor.git
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

**Excel file output:**
- `Aircrafts` sheet → contains all extracted aircrafts data.  
- `Engines` sheet → contains all extracted engines data.  

---

## 🌐 Deployment

You can deploy this app easily using [Streamlit Cloud](https://streamlit.io/cloud).  
After pushing the repository to GitHub:

1. Go to **Streamlit Cloud**.  
2. Connect your GitHub repository.  
3. Select `app.py` as the entry point.  
4. Deploy and share the link with others.  

---

