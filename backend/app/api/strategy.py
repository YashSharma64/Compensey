import logging
import time
from fastapi import APIRouter, HTTPException
from app.schemas.strategy import StrategyRequest, StrategyResponse
from app.services.strategy import generate_strategic_response
import asyncio

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/strategy", response_model=StrategyResponse)
async def strategic_outlook(request: StrategyRequest):
    start_time = time.time()
    logger.info(f"[strategy] Request: {request.company_a} vs {request.company_b}")
    
    try:
        await asyncio.sleep(1.5)
        answer = generate_strategic_response(
            request.company_a, request.company_b,
            request.metrics_a, request.metrics_b,
            request.question, request.drivers,
        )
        logger.info(f"[strategy] Complete in {time.time() - start_time:.2f}s")
        return StrategyResponse(answer=answer)
    except Exception as e:
        logger.error(f"[strategy] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Strategic engine error: {str(e)}")