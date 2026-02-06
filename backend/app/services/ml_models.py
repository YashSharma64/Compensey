import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.pipeline import Pipeline
from app.services.data_loader import load_company_data
from app.services.feature_engineer import prepare_features

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
model_paths = {
    "sentiment": os.path.join(MODELS_DIR, "sentiment_model.pkl"),
    "growth": os.path.join(MODELS_DIR, "growth_model.pkl"),
    "anomaly": os.path.join(MODELS_DIR, "anomaly_model.pkl"),
}

def train_and_save_models():
    """
    Trains models on the mock data and saves them to .pkl files.
    This is a startup routine for this demo.
    """
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)

    # Load data for training (concatenate both mock datasets)
    try:
        df1 = load_company_data("Zomato") # Loads company_a
        df2 = load_company_data("Swiggy") # Loads company_b
        df = pd.concat([df1, df2], ignore_index=True)
        df = prepare_features(df)
    except Exception as e:
        print(f"Error loading training data: {e}")
        return

    # 1. Sentiment Model
    # Predict rating based on review text
    sentiment_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
        ('clf', LogisticRegression())
    ])
    sentiment_pipeline.fit(df['review_text'].fillna(""), df['rating'])
    with open(model_paths['sentiment'], 'wb') as f:
        pickle.dump(sentiment_pipeline, f)
    
    # 2. Growth Model
    # Predict trend_index (proxy for growth/time) based on rating & length
    # This is a bit contrived for the demo, but shows the mechanics
    features = df[['rating', 'review_length']]
    target = df['trend_index']
    growth_model = RandomForestRegressor(n_estimators=100, random_state=42)
    growth_model.fit(features, target)
    with open(model_paths['growth'], 'wb') as f:
        pickle.dump(growth_model, f)
        
    # 3. Anomaly Model
    # Detect anomalous reviews (e.g. spam or bot)
    anomaly_model = IsolationForest(contamination=0.1, random_state=42)
    anomaly_model.fit(features)
    with open(model_paths['anomaly'], 'wb') as f:
        pickle.dump(anomaly_model, f)

    print("Models trained and saved.")

def load_models():
    """Load models from disk. Train if missing."""
    models = {}
    
    # Check if models exist, if not train them
    if not all(os.path.exists(p) for p in model_paths.values()):
        print("Models missing. Training now...")
        train_and_save_models()
        
    for name, path in model_paths.items():
        with open(path, 'rb') as f:
            models[name] = pickle.load(f)
            
    return models

# Global loader to be used by API
models = load_models()

def get_sentiment_score(texts, model):
    """Returns average predicted rating (normalized 0-1)"""
    if not texts:
        return 0.5
    preds = model.predict(texts)
    # ratings are 1-5, normalize to 0-1
    avg_rating = preds.mean()
    return (avg_rating - 1) / 4.0

def get_risk_score(features, model):
    """Returns percentage of anomalies found"""
    if features.empty:
        return 0.0
    # -1 is anomaly, 1 is normal
    preds = model.predict(features)
    anomalies = (preds == -1).sum()
    return anomalies / len(preds)
