from fastapi import APIRouter, HTTPException
from app.schemas.compare import CompareRequest, CompareResponse
from app.services.data_loader import load_company_data
from app.services.feature_engineer import prepare_features, calculate_growth_score
from app.services.ml_models import models, get_sentiment_score, get_risk_score
from app.services.explain import explain_decision, get_shap_feature_importance

router = APIRouter()

@router.post("/compare", response_model=CompareResponse)
async def compare_companies(request: CompareRequest):
    try:
        # 1. Load Data
        df_a = load_company_data(request.company_a)
        df_b = load_company_data(request.company_b)
        
        # 2. Feature Engineering
        df_a = prepare_features(df_a)
        df_b = prepare_features(df_b)
        
        # 3. Model Inference
        # Sentiment
        sent_a = get_sentiment_score(df_a['review_text'].fillna(""), models['sentiment'])
        sent_b = get_sentiment_score(df_b['review_text'].fillna(""), models['sentiment'])
        
        # Growth
        growth_a = calculate_growth_score(df_a)
        growth_b = calculate_growth_score(df_b)
        
        # Anomaly / Risk
        feat_a = df_a[['rating', 'review_length']]
        feat_b = df_b[['rating', 'review_length']]
        
        risk_a = get_risk_score(feat_a, models['anomaly'])
        risk_b = get_risk_score(feat_b, models['anomaly'])
        
        # 4. Determine Winner (Simple Weighted Score)
        # Higher sentiment, Higher growth, Lower risk = Better
        score_a = (sent_a * 0.4) + (growth_a * 0.4) + ((1 - risk_a) * 0.2)
        score_b = (sent_b * 0.4) + (growth_b * 0.4) + ((1 - risk_b) * 0.2)
        
        winner = request.company_a if score_a > score_b else request.company_b
        
        # 5. Explainability
        metrics_a = {'sentiment': sent_a, 'growth': growth_a, 'risk': risk_a}
        metrics_b = {'sentiment': sent_b, 'growth': growth_b, 'risk': risk_b}
        
        explanations = explain_decision(request.company_a, request.company_b, metrics_a, metrics_b)
        
        # SHAP insight (using Company A as the baseline example)
        shap_insight = get_shap_feature_importance(models['growth'], feat_a)
        
        return CompareResponse(
            winner=winner,
            sentiment_score_a=round(sent_a, 2),
            sentiment_score_b=round(sent_b, 2),
            growth_score_a=round(growth_a, 2),
            growth_score_b=round(growth_b, 2),
            explanation=explanations,
            shap_insight=shap_insight
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
