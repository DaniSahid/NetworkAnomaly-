# Personal Data Exposure Checker
### CSC662 — Computer Security Awareness Project | UiTM 2026

A Streamlit app that checks password exposure using the Have I Been Pwned
public API, and lets users explore the full breach database — no API key required.

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open: **http://localhost:8501**

---

## Deploy Free (Streamlit Community Cloud)

1. Push this folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo, set `app.py` as entry point, deploy

---

## Features

### Tab 1 — Password Breach Check
- Checks if a password appears in 10+ billion known breached passwords
- Uses k-Anonymity: only first 5 chars of SHA-1 hash sent, password never exposed
- Password strength analyser with actionable feedback
- Shows how many times the password has been seen in breaches

### Tab 2 — Breach Database Explorer
- Live data from HIBP: 700+ known breaches
- Search by site name
- Filter by exposed data type (passwords, credit cards, IDs, etc.)
- Sorts by most affected, most recent, or alphabetical
- Highlights high-risk breaches in red

### Tab 3 — About
- Explains k-Anonymity
- Documents all APIs used (all free, no key required)
- Lists key awareness lessons

---

## APIs Used (All Free, No Key Required)

| API | URL |
|---|---|
| Pwned Passwords | `https://api.pwnedpasswords.com/range/{prefix}` |
| All Breaches | `https://haveibeenpwned.com/api/v3/breaches` |
| Single Breach | `https://haveibeenpwned.com/api/v3/breach/{name}` |

---

## Project Structure

```
data_exposure_checker/
├── app.py            — Main Streamlit application
├── requirements.txt  — Python dependencies
└── README.md         — This file
```

---

## Disclaimer

For educational purposes only. No user data is stored or transmitted beyond
what is described in the k-Anonymity explanation above.
