# CompenseyAI

> **CompenseyAI is a production-minded competitor intelligence system that turns public review signals into an explainable A vs B benchmark and a consulting-style strategic brief.**

CompenseyAI compares two companies end-to-end: data ingestion → feature engineering → ML scoring → explainability → decision logic → API delivery → UI presentation. The goal is to show how you build a business-relevant ML system that is interpretable, testable, and deployable in principle (not a black-box demo).

---

## 🎯 Project Goal

The goal of this project is to demonstrate:
- **End-to-end AI/ML system design**
- **Real model training and inference**
- **Explainable decision-making** (no black-box AI)
- **Clean full-stack architecture**
- **Business-oriented thinking** (McKinsey-style benchmarking)

*Note: This is not a chatbot, not an LLM-only app, and not a flashy demo.*

---

## ✅ What This System Does (End-to-End)

1. **Inputs**
   - Select `company_a` and `company_b` from the UI (or call the API directly).
2. **Data pipeline**
   - Loads public-style review datasets from `data/` (or generates mock data if missing).
   - Cleans/standardizes fields and produces ML-ready features.
3. **ML scoring (three lenses)**
   - **Sentiment**: text-based sentiment signal.
   - **Growth**: momentum-style signal from engineered activity/ratings patterns.
   - **Risk / stability**: anomaly/volatility style signal.
4. **Decision + explainability**
   - Compares A vs B, produces a winner and the drivers behind the result (including SHAP-style attribution where applicable).
5. **Strategic synthesis ("McKinsey-style" output)**
   - Generates a concise executive brief that ties together the user question, metric deltas, trade-offs, and risks.
6. **Delivery**
   - Backend exposes clean REST endpoints (`/compare`, `/strategy`).
   - Frontend renders the benchmark + strategic brief.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites
- Python 3.10+
- Node.js & npm
- Git

### 1. Backend Setup (The Core)

The backend handles data processing, ML model training, and the API.

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment (Recommended)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

*Note: The system will automatically check for data files. If they are empty, it will generate mock data and train the models on startup.*

### 2. Frontend Setup (The UI)
*(Assuming you are in the project root)*

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The UI should now be accessible (usually at `http://localhost:5173`).

---

## 🧱 Architecture

```
graph TD
    Client[Frontend (React)] -->|REST API| API[Backend (FastAPI)]
    API --> Pipeline[Data + Feature Pipeline]
    Pipeline --> Models[ML Models (scikit-learn)]
    Models --> Explain[Explainability (SHAP/attributions)]
    API --> Decision[Decision + Strategy Engine]
    Pipeline --> Data[CSV Datasets in data/]
```

Design choices that mirror real systems:
- Backend is the core: data/ML/decision logic lives server-side.
- API-first: the UI is a consumer of stable endpoints.
- Explainability is a first-class output (not an afterthought).

---

## 🧰 Tech Stack

### Backend
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Data & ML**: pandas, NumPy, scikit-learn
- **Explainability**: SHAP (with `matplotlib`, `ipython`)
- **Runtime**: uvicorn

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS
- **State & UI**: idiomatic React components and hooks

---

## 📊 ML Decision Logic (How the Output is Produced)

The system is intentionally designed to produce **decision-quality outputs**, not just raw predictions.

1. **Signals (measurable scores)**
   - Sentiment score
   - Growth score
   - Risk/stability score
2. **Comparative reasoning (A vs B)**
   - Computes deltas and identifies leaders per dimension.
   - Detects patterns (trade-off vs parity vs clear leader).
3. **Explainability ("why")**
   - Uses SHAP-style insights to highlight influential features where applicable.
4. **Strategic synthesis ("so what")**
   - Produces an integrated, concise brief:
     - Executive view
     - Key insight (metric deltas)
     - Recommendation (what to do next)
     - Risks and next validation step

---

## 📊 Data & ML Strategy

### Data Sources
- **Customer Reviews**: CSV datasets located in `data/`.
- **Mock Data**: If no data is found, the system auto-generates synthetic review data (`debug_models.py` / `ml_models.py` logic) to demonstrate functionality.
- **Ratings & Metadata**: Used for sentiment and score aggregation.

### ML Models
| Model Type | Algorithm | Output |
| :--- | :--- | :--- |
| **Sentiment** | TF-IDF + Logistic Regression | Sentiment Score |
| **Growth** | RandomForest or XGBoost | Growth Score |
| **Stability** | IsolationForest | Anomaly / Risk Signal |

*All models are trained, evaluated, and saved as `.pkl` files in `backend/models/`.*

### 🔍 Explainability
**SHAP** (SHapley Additive exPlanations) is used to explain:
- Which features influenced the comparison.
- Why one company scored higher than the other.
*Explainability is a core feature, not optional.*

### ✅ How We Evaluate (Credibility)

The sentiment model is evaluated with a simple **train/test split**:
- **Split**: 80% train / 20% test (`random_state=42`)
- **Metrics**: Accuracy and Macro-F1

During training, the backend logs:
`[eval] sentiment_model accuracy=... macro_f1=... (test_size=0.2)`

This keeps the system explainable and lightweight while still providing measurable performance evidence.

---

## 📂 Folder Structure

```
compensey-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/       # ML & Data Logic
│   │   └── schemas/
│   ├── requirements.txt
│   ├── models/             # Saved .pkl models
│   └── venv/               # Virtual Environment
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── data/                   # Data Store (CSV)
```

---

## 📤 API Design

### Core Endpoint: `POST /compare`

**Request**

```json
{
  "company_a": "Zomato",
  "company_b": "Swiggy"
}
```

**Response**  (matches `CompareResponse` in `backend/app/schemas/compare.py`)

```json
{
  "winner": "Swiggy",
  "sentiment_score_a": 68.12,
  "sentiment_score_b": 61.45,
  "growth_score_a": 72.33,
  "growth_score_b": 65.10,
  "explanation": [
    "Swiggy leads in customer satisfaction by 6.7%.",
    "Swiggy is accelerating faster based on review trends.",
    "Swiggy shows more consistent user feedback patterns."
  ],
  "shap_insight": "The main driver for the growth score is Customer Rating."
}
```

### Strategic Outlook Endpoint: `POST /strategy`

**Request**

```json
{
  "company_a": "Zomato",
  "company_b": "Swiggy",
  "metrics_a": {"sentiment": 85.0, "growth": 72.3, "risk": 0.18},
  "metrics_b": {"sentiment": 78.0, "growth": 68.5, "risk": 0.24},
  "question": "Who will win in the long term?"
}
```

**Response**

```json
{
  "answer": "Executive view (recommended action, next 6–12 months): Zomato vs Swiggy...\nKey insight: ...\nRecommendation: ..."
}
```

---

## ✅ Why Compensey?
- **Full-stack**: Covers the entire development lifecycle.
- **ML-first**: Real implementation of Machine Learning, not just API wrappers.
- **Explainable**: Focuses on the "Why", a critical business requirement.
- **Business-focused**: Solves a real-world problem (Competitive Intelligence).
- **Defensible**: Built on solid engineering principles, easy to discuss in interviews.
