import shap
import numpy as np
import os
from typing import List, Dict

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def _template_explanation(company_a: str, company_b: str, a_metrics: Dict, b_metrics: Dict) -> List[str]:
    """
    Fallback: simple template-based explanation using the ML scores.
    Used when Gemini is unavailable.
    """
    explanations = []

    sent_a = float(a_metrics['sentiment'])
    sent_b = float(b_metrics['sentiment'])
    if sent_a > sent_b:
        diff = (sent_a - sent_b) * 100
        explanations.append(f"{company_a} scores higher in customer sentiment by {diff:.1f}% based on review text analysis (TF-IDF + Logistic Regression).")
    else:
        diff = (sent_b - sent_a) * 100
        explanations.append(f"{company_b} leads in customer satisfaction by {diff:.1f}% based on review text analysis (TF-IDF + Logistic Regression).")

    growth_a = float(a_metrics['growth'])
    growth_b = float(b_metrics['growth'])
    if growth_a > growth_b:
        explanations.append(f"{company_a} shows stronger review volume and engagement growth momentum (Random Forest growth score: {growth_a:.2f} vs {growth_b:.2f}).")
    else:
        explanations.append(f"{company_b} is accelerating faster based on review volume trends (Random Forest growth score: {growth_b:.2f} vs {growth_a:.2f}).")

    risk_a = float(a_metrics['risk'])
    risk_b = float(b_metrics['risk'])
    if risk_a < risk_b:
        explanations.append(f"{company_a} shows lower anomaly rate ({risk_a:.2f} vs {risk_b:.2f}), indicating more stable and consistent customer feedback (Isolation Forest).")
    else:
        explanations.append(f"{company_b} exhibits lower anomaly rate ({risk_b:.2f} vs {risk_a:.2f}), indicating more consistent user feedback patterns (Isolation Forest).")

    return explanations


def explain_decision(
    company_a: str,
    company_b: str,
    a_metrics: Dict,
    b_metrics: Dict,
    winner: str,
    shap_drivers: List[str] = None
) -> List[str]:
    """
    Generates 3 natural-language bullet-point explanations for the comparison decision.

    Flow:
      ML scores (computed upstream) → Gemini formats them into professional English.
      Falls back to template-based explanations if Gemini is unavailable.

    Gemini is ONLY used for presentation — all analysis comes from the ML pipeline.
    """
    shap_drivers = shap_drivers or ["Customer Rating", "Review Length"]

    sent_a = float(a_metrics['sentiment'])
    sent_b = float(b_metrics['sentiment'])
    growth_a = float(a_metrics['growth'])
    growth_b = float(b_metrics['growth'])
    risk_a = float(a_metrics['risk'])
    risk_b = float(b_metrics['risk'])

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")

            prompt = f"""You are a data analyst at a top strategy consulting firm. Convert the following \
machine learning model outputs into exactly 3 concise, professional bullet-point insights (plain text, no markdown).

Companies: {company_a} vs {company_b}
Winner declared by ML models: {winner}

ML Model Scores (all computed by scikit-learn, do NOT invent values):
- Sentiment (TF-IDF + Logistic Regression): {company_a}={sent_a:.2f}, {company_b}={sent_b:.2f}
- Growth (Random Forest): {company_a}={growth_a:.2f}, {company_b}={growth_b:.2f}
- Risk/Anomaly (Isolation Forest, lower=better): {company_a}={risk_a:.2f}, {company_b}={risk_b:.2f}
- SHAP key drivers: {', '.join(shap_drivers)}

Rules:
1. Write exactly 3 sentences, one per line (no bullet symbols, no numbering, no markdown).
2. Each sentence must reference the exact numeric scores above.
3. Do NOT add any opinion or data not derived from the scores above.
4. Keep language concise, professional, and grounded in the numbers.
"""
            response = model.generate_content(prompt)
            if response.text and response.text.strip():
                lines = [l.strip() for l in response.text.strip().splitlines() if l.strip()]
                if lines:
                    return lines[:3] if len(lines) >= 3 else lines
        except Exception as e:
            print(f"[explain] Gemini unavailable, using template fallback: {e}")

    # Template fallback
    return _template_explanation(company_a, company_b, a_metrics, b_metrics)


def get_shap_feature_importance(model, feature_data) -> List[str]:
    """
    Returns top features influencing the Growth model (via SHAP TreeExplainer).
    """
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(feature_data)

        feature_names = ['Customer Rating', 'Review Detail (Length)']

        if isinstance(shap_values, list):
            vals = np.abs(shap_values[0]).mean(0)
        else:
            vals = np.abs(shap_values).mean(0)

        importance = list(zip(feature_names, vals))
        importance.sort(key=lambda x: x[1], reverse=True)

        return [importance[0][0], importance[1][0] if len(importance) > 1 else importance[0][0]]
    except Exception as e:
        print(f"[shap] SHAP EXCEPTION: {e}")
        return ["Overall Sentiment Trend", "Review Length"]
