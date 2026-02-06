import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def load_company_data(company_name: str) -> pd.DataFrame:
    """
    Loads review data for a given company.
    In a real app, this might query a DB or scrape a URL.
    For this demo, we map company names to local CSV files.
    """
    company_name = company_name.lower()
    
    # Simple mapping for demo purposes
    if "zomato" in company_name:
        filename = "company_a_reviews.csv"
    elif "swiggy" in company_name:
        filename = "company_b_reviews.csv"
    else:
        # Fallback for demo: randomly pick one if name doesn't match
        # In production this would error out
        filename = "company_a_reviews.csv"

    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found for {company_name}")

    df = pd.read_csv(filepath)
    return df
