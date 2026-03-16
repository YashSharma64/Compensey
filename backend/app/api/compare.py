import hashlib
from fastapi import APIRouter, HTTPException
from app.schemas.compare import CompareRequest, CompareResponse
from app.services.data_loader import load_company_data
from app.services.feature_engineer import prepare_features, calculate_growth_score
from app.services.ml_models import models, get_sentiment_score, get_risk_score
from app.services.explain import explain_decision, get_shap_feature_importance

router = APIRouter()


def _get_hash(s: str) -> float:
    """Deterministic hash to 0.0-1.0 range for POC data differentiation."""
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16) % 100 / 100.0


@router.post("/compare", response_model=CompareResponse)
async def compare_companies(request: CompareRequest):
    try:
        # ── 1. Load Data ────────────────────────────────────────────────────
        df_a = load_company_data(request.company_a)
        df_b = load_company_data(request.company_b)

        # ── 2. Feature Engineering ──────────────────────────────────────────
        df_a = prepare_features(df_a)
        df_b = prepare_features(df_b)

        # ── 3. ML Model Inference ───────────────────────────────────────────
        # Sentiment (TF-IDF + Logistic Regression)
        sent_a = get_sentiment_score(df_a["review_text"].fillna(""), models["sentiment"])
        sent_b = get_sentiment_score(df_b["review_text"].fillna(""), models["sentiment"])

        # Growth (Random Forest)
        growth_a = calculate_growth_score(df_a)
        growth_b = calculate_growth_score(df_b)

        # Anomaly / Risk (Isolation Forest)
        feat_a = df_a[["rating", "review_length"]]
        feat_b = df_b[["rating", "review_length"]]
        risk_a = get_risk_score(feat_a, models["anomaly"])
        risk_b = get_risk_score(feat_b, models["anomaly"])

        # ── 4. POC Noise (deterministic per company name for demo differentiation)
        # In production, replace with real per-company datasets.
        noise_a = (_get_hash(request.company_a) - 0.5) * 0.2
        noise_b = (_get_hash(request.company_b) - 0.5) * 0.2

        sent_a   = max(0, min(100, sent_a   * (1 + noise_a)))
        sent_b   = max(0, min(100, sent_b   * (1 + noise_b)))
        growth_a = max(0, min(100, growth_a * (1 + noise_a * 1.5)))
        growth_b = max(0, min(100, growth_b * (1 + noise_b * 1.5)))
        risk_a   = max(0, min(1,   risk_a   * (1 - noise_a)))
        risk_b   = max(0, min(1,   risk_b   * (1 - noise_b)))

        # ── 5. Score Aggregation & Winner ───────────────────────────────────
        score_a = (sent_a * 0.4) + (growth_a * 0.4) + ((1 - risk_a) * 0.2)
        score_b = (sent_b * 0.4) + (growth_b * 0.4) + ((1 - risk_b) * 0.2)
        winner  = request.company_a if score_a > score_b else request.company_b

        metrics_a = {"sentiment": sent_a, "growth": growth_a, "risk": risk_a}
        metrics_b = {"sentiment": sent_b, "growth": growth_b, "risk": risk_b}

        # ── 6. SHAP Explainability ──────────────────────────────────────────
        shap_drivers  = get_shap_feature_importance(models["growth"], feat_a)
        shap_insight  = f"The main drivers are: {', '.join(shap_drivers)}." if isinstance(shap_drivers, list) else str(shap_drivers)

        # ── 7. Gemini Explanation Layer (presentation only, fallback included)
        # ML scores are passed to Gemini which formats them into professional English.
        explanations = explain_decision(
            request.company_a,
            request.company_b,
            metrics_a,
            metrics_b,
            winner=winner,
            shap_drivers=shap_drivers if isinstance(shap_drivers, list) else [],
        )

        return CompareResponse(
            winner=winner,
            sentiment_score_a=round(sent_a,   2),
            sentiment_score_b=round(sent_b,   2),
            growth_score_a   =round(growth_a, 2),
            growth_score_b   =round(growth_b, 2),
            risk_score_a     =round(risk_a,   4),
            risk_score_b     =round(risk_b,   4),
            explanation=explanations,
            shap_insight=shap_insight,
            raw_drivers=shap_drivers if isinstance(shap_drivers, list) else [],
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
