from pydantic import BaseModel
from typing import Dict, List, Optional

class StrategyRequest(BaseModel):
    company_a: str
    company_b: str
    metrics_a: Dict[str, float]
    metrics_b: Dict[str, float]
    question: str
    drivers: Optional[List[str]] = None

class StrategyResponse(BaseModel):
    answer: str
