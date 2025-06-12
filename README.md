# 📬 Email Engagement Health Check

An AI-powered app that analyzes email threads to determine engagement, sentiment, responsiveness, and risk using Google Gemini and Gmail API. Built with **Python**, **Streamlit**, and **SQLiteCloud**.

---

## 🚀 Features

- 🔐 OAuth2-based Gmail authentication
- 📥 Fetches full **email threads** (not just individual messages)
- 🧠 Uses **Gemini AI** to classify:
  - Engagement Score (High / Medium / Low)
  - Sentiment (Positive / Neutral / Negative)
  - Responsiveness (Reply time patterns)
  - Relationship Quality (e.g., healthy, cold, risky)
  - Risk Alerts (e.g., follow-ups ignored, unhappy tone)
- 📊 Visual dashboard with filters and expandable thread views
- 🧪 Easily seed and analyze synthetic data
- ☁️ Backed by **SQLiteCloud** for persistent and remote DB access

---

## 📂 Project Structure

```
email_engagement_healthcheck/
│
├── main.py                # Streamlit app UI
├── analyzer.py            # Gemini API integration
├── gmail_auth.py          # Gmail authentication logic
├── gmail_fetcher.py       # Fetch full threads from Gmail
├── db.py                  # SQLiteCloud DB setup and helpers
├── test_fetch_store.py    # Email fetch + DB test
├── test_analyzer.py       # Gemini analyzer test
├── test_seed_data.py      # Seed synthetic threads into DB
├── .env                   # Secrets and config
├── requirements.txt       # Python dependencies
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. 🔧 Clone the Repository

```bash
git clone https://github.com/your-username/email-engagement-healthcheck.git
cd email-engagement_healthcheck
```

### 2. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. 🗝️ Configure Environment Variables

Create a `.env` file:

```env
SQLITECLOUD_URL=sqlitecloud://<your-db-url>
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
```

### 4. 🔐 Set Up Gmail API

- Download `credentials.json` from Google Cloud Console
- Place it in the project root
- First run will prompt authorization

### 5. ▶️ Run the App

```bash
streamlit run main.py
```

---

## 🧪 Testing & Sample Data

To seed realistic test data:

```bash
python test_seed_data.py
```

Then analyze in the app:

```bash
streamlit run main.py
```

Or run directly:

```bash
python test_analyzer.py
```

---


---

## 📌 TODO / Roadmap

- [ ] Add CSV export
- [ ] UI polish: tags for sentiment/risk
- [ ] Extend to Outlook and other email providers
- [ ] Add tests with synthetic JSON imports

---
