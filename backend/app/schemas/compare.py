from pydantic import BaseModel
from typing import List

class CompareRequest(BaseModel):
    company_a: str
    company_b: str

class CompareResponse(BaseModel):
    winner: str
    sentiment_score_a: float
    sentiment_score_b: float
    growth_score_a: float
    growth_score_b: float
    risk_score_a: float
    risk_score_b: float
    explanation: List[str]
    shap_insight: str

