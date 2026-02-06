# CompenseyAI

> **CompenseyAI automates early-stage competitor benchmarking using explainable machine learning models and publicly available data to support data-driven business decisions.**

CompenseyAI is an AI/ML competitor intelligence tool that compares two competing companies using publicly available data, applies trained machine learning models to generate explainable insights, and presents the result through a minimal professional UI.

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
- **Data & ML**: Pandas, NumPy, scikit-learn
- **Explainability**: SHAP (requires `matplotlib`, `ipython`)
- **Runtime**: `uvicorn`

### Frontend
- **Framework**: React
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Visualization**: Chart.js or Recharts

---

## 🧱 System Architecture

```
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

## ✅ Why Compensey?
- **Full-stack**: Covers the entire development lifecycle.
- **ML-first**: Real implementation of Machine Learning, not just API wrappers.
- **Explainable**: Focuses on the "Why", a critical business requirement.
- **Business-focused**: Solves a real-world problem (Competitive Intelligence).
- **Defensible**: Built on solid engineering principles, easy to discuss in interviews.
