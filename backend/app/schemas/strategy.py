from pydantic import BaseModel
from typing import Dict

class StrategyRequest(BaseModel):
    company_a: str
    company_b: str
    metrics_a: Dict[str, float]
    metrics_b: Dict[str, float]
    question: str

class StrategyResponse(BaseModel):
    answer: str
