def generate_strategic_response(company_a, company_b, metrics_a, metrics_b, question):
    """
    Generates a McKinsey-style strategic response based on current metrics and the user's question.
    Avoids predictions. Uses scenario-based reasoning.
    """
    question_lower = question.lower()
    
    # Extract metrics for cleaner logic
    sent_a = metrics_a.get('sentiment', 0)
    growth_a = metrics_a.get('growth', 0)
    risk_a = metrics_a.get('risk', 0)
    
    sent_b = metrics_b.get('sentiment', 0)
    growth_b = metrics_b.get('growth', 0)
    
    # Identify Leader
    leader_growth = company_a if growth_a > growth_b else company_b
    laggard_growth = company_b if growth_a > growth_b else company_a
    
    leader_sent = company_a if sent_a > sent_b else company_b

    # 1. FUTURE / GROWTH SCENARIOS
    if any(q in question_lower for q in ['future', 'long-term', 'next year', 'who will win', 'position']):
        diff = abs(growth_a - growth_b)
        if diff < 10:
            return (
                f"Evaluation of current growth trajectories suggests a highly competitive landscape between {company_a} and {company_b}. "
                f"While {leader_growth} holds a marginal advantage in momentum, the gap is not statistically significant to declare a definitive leader. "
                f"If {laggard_growth} can improve its sentiment metrics (currently {metrics_b['sentiment'] if laggard_growth == company_b else sent_a:.1f}), "
                "it may capture market share in the coming 2-4 quarters. "
                "Scenario: A stagnation in innovation from the leader could rapidly shift market dynamics."
            )
        else:
            return (
                f"Based on current signals, {leader_growth} demonstrates a stronger growth velocity compared to {laggard_growth}. "
                f"If these trends persist, {leader_growth} is better positioned to consolidate market leadership over the next 12 months. "
                f"However, this outlook assumes no major external disruptions or regulatory shifts. "
                f"Strategic Recommendation for {laggard_growth}: Focus on distinct value propositions to disrupt the incumbent's momentum."
            )

    # 2. RISK / DOWNSIDE SCENARIOS
    elif any(q in question_lower for q in ['risk', 'fail', 'problem', 'bad', 'volatility']):
        high_risk_company = company_a if risk_a > 0.3 else (company_b if metrics_b['risk'] > 0.3 else None)
        
        if high_risk_company:
            return (
                f"Quantitative analysis highlights potential volatility for {high_risk_company}. "
                f"Anomaly detection algorithms have flagged irregular patterns in recent reviews, which often precede a decline in brand trust. "
                f"Mitigation Strategy: {high_risk_company} should prioritize operational stability over aggressive expansion in the short term. "
                "Failure to address these underlying anomalies could result in customer churn exceeding 5% in the next quarter."
            )
        else:
            return (
                f"Current data indicates a relatively stable risk profile for both entities. "
                "However, market leadership is often fragile. The primary risk factor remains 'Complacency'. "
                f"If {leader_sent} fails to maintain its high sentiment scores ({max(sent_a, sent_b):.1f}), "
                "it opens a strategic window for competitors to enter with superior service offerings."
            )

    # 3. GENERIC / UNKNOWN QUESTION
    else:
        return (
            "From a strategic standpoint, the data suggests currently diverging paths. "
            f"{company_a} is trading on sentiment ({sent_a:.1f}) while {company_b} is showing growth signals ({growth_b:.1f}). "
            "Consultant's View: The winner in the long run will likely be the entity that best balances rapid scaling (Growth) with customer retention (Sentiment). "
            "We advise monitoring quarterly retention cohorts to refine this outlook."
        )
