import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.pipeline import Pipeline

from app.services.data_loader import load_company_data
from app.services.feature_engineer import prepare_features

# ------------------ Paths ------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATHS = {
    "sentiment": os.path.join(MODELS_DIR, "sentiment_model.pkl"),
    "growth": os.path.join(MODELS_DIR, "growth_model.pkl"),
    "anomaly": os.path.join(MODELS_DIR, "anomaly_model.pkl"),
}

# ------------------ Training ------------------

def train_and_save_models() -> None:
    """
    Trains sentiment, growth, and anomaly models and saves them to disk.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)

    try:
        df = pd.concat(
            [
                load_company_data("Zomato"),
                load_company_data("Swiggy"),
            ],
            ignore_index=True,
        )
        df = prepare_features(df)
    except Exception as e:
        print(f"Error loading training data: {e}")
        return

    # -------- Sentiment Model --------
    sentiment_model = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=1000, stop_words="english")),
            ("clf", LogisticRegression()),
        ]
    )
    sentiment_model.fit(df["review_text"].fillna(""), df["rating"])
    _save_model("sentiment", sentiment_model)

    # -------- Growth Model --------
    X = df[["rating", "review_length"]]
    y = df["trend_index"]

    growth_model = RandomForestRegressor(n_estimators=100, random_state=42)
    growth_model.fit(X, y)
    _save_model("growth", growth_model)

    # -------- Anomaly Model --------
    anomaly_model = IsolationForest(contamination=0.1, random_state=42)
    anomaly_model.fit(X)
    _save_model("anomaly", anomaly_model)

    print("Models trained and saved successfully.")

# ------------------ Loading ------------------

def load_models() -> dict:
    """
    Loads models from disk. Trains them if missing.
    """
    if not all(os.path.exists(path) for path in MODEL_PATHS.values()):
        print("Models missing. Training now...")
        train_and_save_models()

    return {
        name: _load_model(name)
        for name in MODEL_PATHS
    }

def _save_model(name: str, model) -> None:
    with open(MODEL_PATHS[name], "wb") as f:
        pickle.dump(model, f)

def _load_model(name: str):
    with open(MODEL_PATHS[name], "rb") as f:
        return pickle.load(f)

# Global models (loaded once)
models = load_models()

# ------------------ Inference Helpers ------------------

def get_sentiment_score(texts, model) -> float:
    """
    Returns average predicted rating normalized to [0, 1].
    """
    if len(texts) == 0:
        return 0.5

    avg_rating = model.predict(texts).mean()
    return (avg_rating - 1) / 4.0


def get_risk_score(features: pd.DataFrame, model) -> float:
    """
    Returns fraction of anomalous samples.
    """
    if features.empty:
        return 0.0

    preds = model.predict(features)
    return float((preds == -1).mean())
