# CompenseyAI

> **CompenseyAI automates early-stage competitor benchmarking using explainable machine learning models and publicly available data to support data-driven business decisions.**

CompenseyAI is a backend-heavy, full-stack AI/ML competitor intelligence tool that compares two competing companies using publicly available data, applies trained machine learning models to generate explainable insights, and presents the result through a minimal professional UI.

---

## 🎯 Project Goal

The goal of this project is to demonstrate:
- **End-to-end AI/ML system design**
- **Real model training, evaluation, and inference**
- **Explainable decision-making** (no black-box AI)
- **Clean full-stack architecture**
- **Business-oriented thinking** (McKinsey-style benchmarking)

*Note: This is not a chatbot, not an LLM-only app, and not a flashy demo.*

---

## 🧠 Functional Overview

1. **User Selection**: User selects Company A and Company B.
2. **Data Pipeline**: Backend loads structured data for both companies. Data is cleaned and transformed into ML features.
3. **Inference**: Multiple ML models run inference:
    - **Sentiment Analysis**: TF-IDF + Logistic Regression
    - **Growth Comparison**: RandomForest or XGBoost
    - **Stability / Anomaly Signals**: IsolationForest
4. **Decision Engine**: The system determines which company is performing better and *why*.
5. **Presentation**: Results are returned as structured JSON and displayed on the Frontend.

---

## 🧰 Tech Stack

### Backend
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Data Processing**: Pandas, NumPy
- **ML / AI**: scikit-learn
- **Explainability**: SHAP
- **Database**: SQLite (or CSV-based loading)
- **Containerization**: Docker

### Frontend
- **Framework**: React
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Visualization**: Chart.js or Recharts

---

## 🧱 System Architecture

```mermaid
graph TD
    Client[Frontend (React)] -->|REST API| API[Backend (FastAPI - Python)]
    API --> ML[ML Layer (scikit-learn models)]
    ML --> Data[CSV / Structured Datasets]
    
    subgraph Core "Backend is Core"
    API
    ML
    Data
    end
```

The backend is the core of the system. The frontend serves solely to display the results.

---

## 📊 Data & ML Strategy

### Data Sources
- **Customer Reviews**: CSV datasets (e.g., from Play Store / Kaggle).
- **Ratings & Metadata**: Used for sentiment and score aggregation.
- *Why this is acceptable*: Publicly available, real user sentiment, and standard for competitive benchmarking.

### ML Models
| Model Type | Algorithm | Output |
| :--- | :--- | :--- |
| **Sentiment** | TF-IDF + Logistic Regression | Sentiment Score |
| **Growth** | RandomForest or XGBoost | Growth Score |
| **Stability** | IsolationForest | Anomaly / Risk Signal |

*All models are trained, evaluated, and saved as `.pkl` files.*

### 🔍 Explainability
**SHAP** (SHapley Additive exPlanations) is used to explain:
- Which features influenced the comparison.
- Why one company scored higher than the other.
*Explainability is a core feature, not optional.*

---

## 📂 Folder Structure

```
compensey-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── compare.py
│   │   ├── services/
│   │   │   ├── data_loader.py
│   │   │   ├── feature_engineer.py
│   │   │   ├── ml_models.py
│   │   │   └── explain.py
│   │   └── schemas/
│   │       └── compare.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── Result.jsx
│   │   ├── api/
│   │   │   └── compare.js
│   │   ├── components/
│   │   │   └── Navbar.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── data/
│   ├── company_a_reviews.csv
│   ├── company_b_reviews.csv
│   └── README.md
└── models/
    ├── sentiment_model.pkl
    ├── growth_model.pkl
    └── anomaly_model.pkl
```

---

## 📤 API Design

### Core Endpoint: `POST /compare`

**Request:**
```json
{
  "company_a": "Zomato",
  "company_b": "Swiggy"
}
```

**Response:**
```json
{
  "winner": "Swiggy",
  "sentiment_score": 0.68,
  "growth_score": 0.74,
  "explanation": [
    "Higher delivery satisfaction",
    "More stable growth trend"
  ]
}
```

---

## ✅ Why This Project is Strong
- **Full-stack**: Covers the entire development lifecycle.
- **ML-first**: Real implementation of Machine Learning, not just API wrappers.
- **Explainable**: Focuses on the "Why", a critical business requirement.
- **Business-focused**: Solves a real-world problem (Competitive Intelligence).
- **Defensible**: Built on solid engineering principles, easy to discuss in interviews.
