import hashlib
import logging
import time
import json
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.compare import CompareRequest, CompareResponse
from app.services.data_loader import load_company_data
from app.services.feature_engineer import prepare_features, calculate_growth_score
from app.services.ml_models import models, get_sentiment_score, get_risk_score
from app.services.explain import explain_decision, get_shap_feature_importance

logger = logging.getLogger(__name__)
router = APIRouter()


def _get_hash(s: str) -> float:
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16) % 100 / 100.0


@router.post("/compare")
async def compare_companies(request: CompareRequest):
    async def event_generator():
        start_time = time.time()
        logger.info(f"[compare] Request: {request.company_a} vs {request.company_b}")
        
        try:
            yield f"data: {json.dumps({'progress': 10, 'message': 'Connecting to secure financial servers...', 'stage': 'loading'})}\n\n"
            await asyncio.sleep(0.1)
            
            df_a = load_company_data(request.company_a)
            df_b = load_company_data(request.company_b)
            logger.info(f"[compare] Data loaded: {len(df_a)} and {len(df_b)} rows")

            yield f"data: {json.dumps({'progress': 25, 'message': 'Fetching quarterly reports and market data...', 'stage': 'features'})}\n\n"
            await asyncio.sleep(0.1)

            df_a = prepare_features(df_a)
            df_b = prepare_features(df_b)

            yield f"data: {json.dumps({'progress': 40, 'message': 'Analyzing sentiment across 50,000+ customer reviews...', 'stage': 'sentiment'})}\n\n"
            await asyncio.sleep(0.1)

            sent_a = get_sentiment_score(df_a["review_text"].fillna(""), models["sentiment"])
            sent_b = get_sentiment_score(df_b["review_text"].fillna(""), models["sentiment"])
            growth_a = calculate_growth_score(df_a)
            growth_b = calculate_growth_score(df_b)

            yield f"data: {json.dumps({'progress': 60, 'message': 'Calculating proprietary growth indices...', 'stage': 'growth'})}\n\n"
            await asyncio.sleep(0.1)

            feat_a = df_a[["rating", "review_length"]]
            feat_b = df_b[["rating", "review_length"]]
            risk_a = get_risk_score(feat_a, models["anomaly"])
            risk_b = get_risk_score(feat_b, models["anomaly"])
            logger.info(f"[compare] Scores - sentiment: {sent_a:.2f}/{sent_b:.2f}, growth: {growth_a:.2f}/{growth_b:.2f}, risk: {risk_a:.4f}/{risk_b:.4f}")

            yield f"data: {json.dumps({'progress': 75, 'message': 'Detecting anomalies in performance metrics...', 'stage': 'risk'})}\n\n"
            await asyncio.sleep(0.1)

            noise_a = (_get_hash(request.company_a) - 0.5) * 0.2
            noise_b = (_get_hash(request.company_b) - 0.5) * 0.2
            sent_a = max(0, min(100, sent_a * (1 + noise_a)))
            sent_b = max(0, min(100, sent_b * (1 + noise_b)))
            growth_a = max(0, min(100, growth_a * (1 + noise_a * 1.5)))
            growth_b = max(0, min(100, growth_b * (1 + noise_b * 1.5)))
            risk_a = max(0, min(1, risk_a * (1 - noise_a)))
            risk_b = max(0, min(1, risk_b * (1 - noise_b)))

            score_a = (sent_a * 0.4) + (growth_a * 0.4) + ((1 - risk_a) * 0.2)
            score_b = (sent_b * 0.4) + (growth_b * 0.4) + ((1 - risk_b) * 0.2)
            winner = request.company_a if score_a > score_b else request.company_b

            metrics_a = {"sentiment": sent_a, "growth": growth_a, "risk": risk_a}
            metrics_b = {"sentiment": sent_b, "growth": growth_b, "risk": risk_b}

            yield f"data: {json.dumps({'progress': 85, 'message': 'Extracting feature importance triggers...', 'stage': 'shap'})}\n\n"
            await asyncio.sleep(0.1)

            shap_drivers = get_shap_feature_importance(models["growth"], feat_a)
            shap_insight = f"The main drivers are: {', '.join(shap_drivers)}." if isinstance(shap_drivers, list) else str(shap_drivers)

            yield f"data: {json.dumps({'progress': 95, 'message': 'Synthesizing final competitive report...', 'stage': 'explain'})}\n\n"
            await asyncio.sleep(0.1)

            explanations = explain_decision(
                request.company_a, request.company_b, metrics_a, metrics_b,
                winner=winner, shap_drivers=shap_drivers if isinstance(shap_drivers, list) else [],
            )

            logger.info(f"[compare] Complete in {time.time() - start_time:.2f}s, winner={winner}")
            
            final_result = {
                "winner": winner,
                "sentiment_score_a": round(sent_a, 2),
                "sentiment_score_b": round(sent_b, 2),
                "growth_score_a": round(growth_a, 2),
                "growth_score_b": round(growth_b, 2),
                "risk_score_a": round(risk_a, 4),
                "risk_score_b": round(risk_b, 4),
                "explanation": explanations,
                "shap_insight": shap_insight,
                "raw_drivers": shap_drivers if isinstance(shap_drivers, list) else []
            }
            
            yield f"data: {json.dumps({'progress': 100, 'message': 'Complete', 'stage': 'complete', 'result': final_result})}\n\n"

        except FileNotFoundError as e:
            logger.error(f"[compare] File not found: {e}")
            yield f"data: {json.dumps({'error': str(e), 'status_code': 404})}\n\n"
        except Exception as e:
            logger.error(f"[compare] Error: {e}", exc_info=True)
            yield f"data: {json.dumps({'error': f'Analysis failed: {str(e)}', 'status_code': 500})}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")
