import hashlib
import math
import random
import os
import json
from typing import Dict, List, Optional, Tuple

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def _safe_float(value, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _stable_rng(*parts: object) -> random.Random:
    material = "|".join(str(p) for p in parts)
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    seed = int(digest[:16], 16)
    return random.Random(seed)


def _infer_intent(question: str) -> str:
    q = (question or "").strip().lower()
    if any(k in q for k in ("long-term", "long term", "future", "next", "12 months", "year", "win", "position", "outlook")):
        return "outlook"
    if any(k in q for k in ("risk", "downside", "fail", "volatility", "uncertainty", "problem", "fragile")):
        return "risk"
    if any(k in q for k in ("what should", "recommend", "strategy", "should we", "priorit", "focus", "do next", "plan")):
        return "recommendation"
    if any(k in q for k in ("why", "explain", "drivers", "because", "reason")):
        return "drivers"
    return "general"


def _score_label(delta: float, scale: float = 100.0) -> str:
    d = abs(delta)
    if d < 0.04 * scale:
        return "near-parity"
    if d < 0.10 * scale:
        return "edge"
    if d < 0.20 * scale:
        return "meaningful lead"
    return "clear lead"


def _risk_label(r: float) -> str:
    if r < 0.15:
        return "low"
    if r < 0.30:
        return "moderate"
    return "elevated"


def _pick(rng: random.Random, options: Tuple[str, ...]) -> str:
    return options[rng.randrange(len(options))]


def generate_strategic_response(company_a, company_b, metrics_a, metrics_b, question, drivers: Optional[List[str]] = None):
    # Setup Metrics
    metrics_a = metrics_a or {}
    metrics_b = metrics_b or {}

    sent_a = _safe_float(metrics_a.get("sentiment"), 0.0)
    growth_a = _safe_float(metrics_a.get("growth"), 0.0)
    risk_a = _safe_float(metrics_a.get("risk"), 0.0)

    sent_b = _safe_float(metrics_b.get("sentiment"), 0.0)
    growth_b = _safe_float(metrics_b.get("growth"), 0.0)
    risk_b = _safe_float(metrics_b.get("risk"), 0.0)

    company_a = (company_a or "Company A").strip()
    company_b = (company_b or "Company B").strip()
    question = (question or "").strip()
    drivers = drivers or []

    # Dynamic LLM Logic (Gemini)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            prompt = f"""
            You are a top-tier management consultant and data analyst from McKinsey or Bain. Your job is to analyze the following metrics for two companies and provide a concise, hard-hitting strategic outlook.

            Companies:
            - Company A: {company_a}
            - Company B: {company_b}

            Objective Metrics (Derived from Machine Learning models on customer data):
            - {company_a}: Sentiment Score: {sent_a:.1f}, Growth/Momentum Score: {growth_a:.1f}, Risk/Volatility: {_risk_label(risk_a)} (score: {risk_a:.2f})
            - {company_b}: Sentiment Score: {sent_b:.1f}, Growth/Momentum Score: {growth_b:.1f}, Risk/Volatility: {_risk_label(risk_b)} (score: {risk_b:.2f})
            
            Key Insights derived from data elements (SHAP drivers): {', '.join(drivers) if drivers else 'None provided'}
            
            Client's Specific Question: "{question}"

            Task: Write a 4-to-5 sentence "Executive View" answering the client's question based strictly on these metrics. 
            CRITICAL INSTRUCTIONS: 
            1. You MUST include the exact numbers and deltas (e.g., "Company A leads in customer sentiment with a score of {sent_a:.1f} compared to {sent_b:.1f}").
            2. DO NOT use any markdown formatting whatsoever (no **, no #, no bullet points). Return strictly plain text. 
            
            Act as a data-driven analyst—your insights should be explicitly backed by the numerical scores provided above.
            Focus on trade-offs (if one leads in growth but lags in sentiment). 
            End with a single recommended action for someone investing or advising in this space. 
            Write confidently, as an expert consultant. Avoid fluff.
            """
            
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API failed or is not configured correctly: {e}. Falling back to deterministic strategy generation.")
            pass # Fall through to deterministic logic below


    # Fallback Deterministic Logic
    intent = _infer_intent(question)
    rng = _stable_rng(
        company_a, company_b, question,
        ",".join(drivers[:5]),
        round(sent_a, 3), round(growth_a, 3), round(risk_a, 3),
        round(sent_b, 3), round(growth_b, 3), round(risk_b, 3),
    )

    sent_delta = sent_a - sent_b
    growth_delta = growth_a - growth_b
    risk_delta = risk_a - risk_b

    growth_leader = company_a if growth_delta >= 0 else company_b
    sentiment_leader = company_a if sent_delta >= 0 else company_b

    def fmt(x: float) -> str:
        if math.isnan(x) or math.isinf(x):
            return "0.0"
        return f"{x:.1f}"

    def delta_phrase(metric: str, delta: float) -> str:
        label = _score_label(delta)
        direction = "higher" if delta > 0 else "lower"
        if label == "near-parity":
            return f"{metric} is broadly comparable"
        return f"{metric} is {label} ({direction} by ~{fmt(abs(delta))})"

    opener = _pick(rng, ("Executive view", "Board view", "Strategic read"))
    timeframe = _pick(rng, ("next 2–4 quarters", "next 6–12 months", "the coming year"))

    summary_focus = {
        "outlook": "outlook",
        "risk": "risk",
        "recommendation": "recommended action",
        "drivers": "key drivers",
        "general": "positioning",
    }[intent]

    summary = (
        f"{opener} ({summary_focus}, {timeframe}): {company_a} vs {company_b}. "
        f"Signals synthesized from sentiment, growth and risk indicate: "
        f"growth leader = {growth_leader} ({fmt(growth_a)} vs {fmt(growth_b)}), "
        f"sentiment leader = {sentiment_leader} ({fmt(sent_a)} vs {fmt(sent_b)}), "
        f"risk is {_risk_label(risk_a)} vs {_risk_label(risk_b)}."
    )

    insight = (
        f"Key insight: {delta_phrase('growth', growth_delta)}; {delta_phrase('sentiment', sent_delta)}; "
        f"risk is {'higher' if risk_delta > 0 else 'lower' if risk_delta < 0 else 'similar'} for {company_a} by ~{fmt(abs(risk_delta))}."
    )

    driver_line = None
    if drivers:
        cleaned = [d.strip() for d in drivers if isinstance(d, str) and d.strip()]
        if cleaned:
            driver_line = "Drivers: " + "; ".join(cleaned[:2])

    if (growth_delta > 0 and sent_delta < 0) or (growth_delta < 0 and sent_delta > 0):
        tradeoff = "Pattern: one side is winning momentum while the other is winning trust; the winner will be whoever closes their gap first."
    elif abs(growth_delta) < 4.0 and abs(sent_delta) < 4.0:
        tradeoff = "Pattern: near-parity; execution quality and consistency will decide more than positioning."
    else:
        tradeoff = None

    if growth_leader == sentiment_leader:
        leader = growth_leader
        follower = company_b if leader == company_a else company_a
        recommendation = (
            f"Recommendation: {leader} should press advantage by scaling what is repeatable (quality + cadence), not just acquisition. "
            f"{follower} should focus on one wedge: fix experience to close sentiment, or build a distinct growth channel (not imitation)."
        )
    else:
        recommendation = (
            f"Recommendation: {growth_leader} should convert momentum into trust (reduce friction, improve reliability) to avoid a sentiment tax. "
            f"{sentiment_leader} should translate goodwill into a repeatable growth engine (distribution/pricing/partnerships)."
        )

    risk_note = (
        f"Risks: sentiment reversal for the growth leader at scale; growth stalling for the sentiment leader; volatility spikes (today {_risk_label(risk_a)} vs {_risk_label(risk_b)})."
    )

    next_step = _pick(
        rng,
        (
            "Next step: validate drivers behind sentiment (top recurring pain points) and confirm growth durability across multiple periods.",
            "Next step: isolate top 2 sentiment drivers and test one targeted fix; in parallel validate whether growth holds without heavy promotions.",
        ),
    )

    question_wrap = "" if not question else f"In your question ('{question}'), the decision hinge is whether the leader can sustain its advantage while closing its gap."

    parts = [summary, insight]
    if driver_line:
        parts.append(driver_line)
    if tradeoff:
        parts.append(tradeoff)
    parts.extend([recommendation, risk_note, next_step])
    if question_wrap:
        parts.append(question_wrap)

    return "\n".join(parts)

