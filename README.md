# CompenseyAI

> **AI-powered competitor intelligence that turns customer reviews into consulting-grade insights.**

CompenseyAI compares two companies end-to-end using a **compound AI architecture**: deterministic ML models compute hard numeric signals, and a Generative AI layer (Gemini) converts those signals into professional, consulting-style English insights.

This is **not** a prompt-to-LLM app. All decisions are made by the ML pipeline. Gemini is a presentation layer only.

---

## 🎯 Project Goal

Demonstrate a production-minded, full-stack AI/ML system with:
- **Deterministic ML modeling** (scikit-learn)
- **Explainable AI** (SHAP attributions)
- **Compound AI design** (ML → Gemini presentation layer)
- **Clean full-stack architecture** (FastAPI + React)
- **Business-oriented output** (McKinsey-style competitive brief)

---

## ✅ System Pipeline

```
Customer Review Data (CSV)
        ↓
Pandas ETL / Data Cleaning
        ↓
Feature Engineering
        ↓
Machine Learning Models
  - Sentiment:  TF-IDF + Logistic Regression
  - Growth:     Random Forest (trend signal)
  - Risk:       Isolation Forest (anomaly detection)
        ↓
Score Aggregation → Winner
        ↓
SHAP Explainability (key drivers)
        ↓
Gemini API — formats ML scores into consultancy-style English
  (Falls back to deterministic template if Gemini is unavailable)
        ↓
FastAPI Backend  (/compare, /strategy)
        ↓
React + Vite Frontend
```

**Key rule:** Gemini receives the computed scores and SHAP drivers. It cannot invent data or make decisions. All analytics are determined upstream by scikit-learn.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm
- A `GEMINI_API_KEY` (optional — app works without it via fallback)

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your Gemini API key (optional)
cp .env.example .env
# Edit .env: GEMINI_API_KEY=your_key_here

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> On startup, the system checks for trained models. If missing, it trains them automatically on the data in `data/`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

UI available at: **http://localhost:5173**

---

## 🧱 Architecture

| Layer | Technology | Role |
|---|---|---|
| Data | CSV + Pandas | ETL & feature engineering |
| ML Models | scikit-learn | Sentiment, growth, risk scoring |
| Explainability | SHAP | Feature importance attribution |
| Reasoning | Deterministic logic | Winner decision + scoring |
| Presentation | Gemini API | Natural language explanation (with fallback) |
| Backend | FastAPI + uvicorn | REST API |
| Frontend | React + Vite + Tailwind | UI |

---

## 📊 ML Models

| Signal | Algorithm | Output |
|---|---|---|
| **Sentiment** | TF-IDF + Logistic Regression | Sentiment score [0–1] |
| **Growth** | Random Forest Regressor | Growth momentum score |
| **Risk** | Isolation Forest | Anomaly rate [0–1] |

All models are trained on startup and saved as `.pkl` in `backend/models/`.

Evaluation is logged on startup:
```
[eval] sentiment_model accuracy=0.82 macro_f1=0.79 (test_size=0.2)
```

---

## 🔍 Explainability

**SHAP (SHapley Additive exPlanations)** is used on the Random Forest growth model to identify the top drivers influencing each comparison. These are surfaced in the API response and injected into the Gemini prompt so the strategic memo directly references them.

---

## 🤖 Gemini Explanation Layer

After ML scores are computed, Gemini is called with a strict prompt containing only the ML outputs:

```
Sentiment (TF-IDF + LR): CompanyA=0.91, CompanyB=0.96
Growth (RF): CompanyA=0.49, CompanyB=0.56
Risk (Isolation Forest): CompanyA=0.47, CompanyB=0.52
SHAP drivers: Review Detail (Length), Customer Rating
```

Gemini formats these into professional English bullets — no decisions, no invented data.

**Fallback:** If `GEMINI_API_KEY` is missing or quota is exceeded, the system automatically uses a deterministic template engine that produces the same structured, consultancy-style output using the ML scores directly.

---

## 📤 API Endpoints

### `POST /compare`

```json
{ "company_a": "Zomato", "company_b": "Swiggy" }
```

Response includes winner, sentiment/growth/risk scores, Gemini-formatted explanations, SHAP insight, and raw drivers.

### `POST /strategy`

```json
{
  "company_a": "Swiggy", "company_b": "Zomato",
  "metrics_a": { "sentiment": 0.96, "growth": 0.56, "risk": 0.52 },
  "metrics_b": { "sentiment": 0.91, "growth": 0.49, "risk": 0.47 },
  "question": "Who wins in the long term?",
  "drivers": ["Review Detail (Length)", "Customer Rating"]
}
```

Returns a consulting-style strategic memo grounded in the ML scores.

---

## 📂 Folder Structure

```
compensey/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/          # compare.py, strategy.py
│   │   ├── services/     # ml_models, explain, strategy, data_loader, feature_engineer
│   │   └── schemas/
│   ├── data/             # CSV review datasets (Zomato, Swiggy, Uber, Lyft)
│   ├── models/           # Saved .pkl model files
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── pages/        # Home.jsx, Result.jsx
    │   └── components/
    └── package.json
```

---

## 📦 Datasets

Currently bundled:
- `zomato_clean.csv` / `swiggy_clean.csv` — primary MVP dataset
- `uber_clean.csv` / `lyft_clean.csv` — ready for future comparison

The pipeline is **data-agnostic** — adding a new company only requires dropping a CSV in `data/` and updating the name mapping in `data_loader.py`.

---

## ✅ Running Tests

```bash
cd backend
source venv/bin/activate
pytest tests/
```

---

## 🔮 Future Extensions

- Automated review scraping (Trustpilot, App Store)
- Deployment: Vercel (frontend) + Render (backend)
- Additional company pair datasets
