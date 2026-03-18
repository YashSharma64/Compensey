import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def load_company_data(company_name: str) -> pd.DataFrame:
    """
    Loads review data for a given company from CSV files.
    """
    company_name = company_name.lower()
    
    # Simple mapping for demo purposes
    if "zomato" in company_name:
        candidates = ["zomato.csv", "zomato_clean.csv"]
    elif "swiggy" in company_name:
        candidates = ["swiggy.csv", "swiggy_clean.csv"]
    else:
        # Fallback for demo: randomly pick one if name doesn't match
        # In production this would error out
        candidates = ["zomato.csv", "zomato_clean.csv"]

    filepath = None
    for name in candidates:
        candidate_path = os.path.join(DATA_DIR, name)
        if os.path.exists(candidate_path):
            filepath = candidate_path
            break

    if filepath is None:
        raise FileNotFoundError(f"Data file not found for {company_name}. Expected one of: {', '.join(candidates)} in {DATA_DIR}")

    df = pd.read_csv(filepath)
    required = {"review_text", "rating", "date"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(
            f"CSV schema mismatch for {company_name}: missing columns {sorted(missing)}. "
            f"Expected columns: review_text,rating,date"
        )
    return df
