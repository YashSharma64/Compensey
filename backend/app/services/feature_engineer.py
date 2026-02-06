import pandas as pd
import numpy as np

def prepare_features(df: pd.DataFrame):
    """
    Cleans data and engineering features for ML models.
    """
    # 1. Basic Cleaning
    df['date'] = pd.to_datetime(df['date'])
    df['review_length'] = df['review_text'].fillna("").apply(len)
    
    # 2. Sentiment Features (Placeholder for TF-IDF logic which is usually in the model pipeline)
    # We will just pass the raw text to the model pipeline which includes Vectorizer
    
    # 3. Growth Features
    # Calculate daily review count as a proxy for growth/traction
    daily_counts = df.groupby('date').size().reset_index(name='daily_reviews')
    # Merge back to have it as a feature (propagated) - simplistic approach
    # For a real growth model, we might feed the timeseries itself, but here we'll 
    # just create a 'trend_index' based on time
    df['trend_index'] = (df['date'] - df['date'].min()).dt.days
    
    return df

def calculate_growth_score(df: pd.DataFrame) -> float:
    """
    Simple heuristic growth score based on recent review volume trend.
    """
    # Compare last 7 days vs previous 7 days
    recent_date = df['date'].max()
    last_week = df[df['date'] > (recent_date - pd.Timedelta(days=7))]
    prev_week = df[(df['date'] <= (recent_date - pd.Timedelta(days=7))) & 
                   (df['date'] > (recent_date - pd.Timedelta(days=14)))]
    
    count_last = len(last_week)
    count_prev = len(prev_week)
    
    if count_prev == 0:
        return 0.8 # Default strong start if new
        
    growth_ratio = count_last / count_prev
    # Normalize to 0-1 range roughly
    score = min(max(growth_ratio * 0.5, 0.0), 1.0)
    return float(score)
