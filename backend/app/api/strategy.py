from fastapi import APIRouter, HTTPException
from app.schemas.strategy import StrategyRequest, StrategyResponse
from app.services.strategy import generate_strategic_response
import asyncio

router = APIRouter()

@router.post("/strategy", response_model=StrategyResponse)
async def strategic_outlook(request: StrategyRequest):
    try:
        # Processing delay for complex scenario analysis
        await asyncio.sleep(1.5)
        
        answer = generate_strategic_response(
            request.company_a, 
            request.company_b, 
            request.metrics_a, 
            request.metrics_b, 
            request.question
        )
        
        return StrategyResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategic engine error: {str(e)}")