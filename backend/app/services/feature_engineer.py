import pandas as pd

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning and feature preparation for ML models.
    """
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])
    df["review_length"] = df["review_text"].fillna("").str.len()

    # Time-based proxy for growth/trend
    df["trend_index"] = (df["date"] - df["date"].min()).dt.days

    return df


def calculate_growth_score(df: pd.DataFrame) -> float:
    """
    Heuristic growth score based on recent vs previous week review volume.
    """
    recent_date = df["date"].max()

    last_week_count = (df["date"] > recent_date - pd.Timedelta(days=7)).sum()
    prev_week_count = (
        (df["date"] <= recent_date - pd.Timedelta(days=7)) &
        (df["date"] > recent_date - pd.Timedelta(days=14))
    ).sum()

    if prev_week_count == 0:
        return 0.8

    growth_ratio = last_week_count / prev_week_count
    return float(min(max(growth_ratio * 0.5, 0.0), 1.0))
