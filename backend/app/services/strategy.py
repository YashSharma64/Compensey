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
        # Use current metrics to shape the narrative instead of a single fixed template.
        growth_gap = abs(growth_a - growth_b)
        sentiment_gap = abs(sent_a - sent_b)

        # Case A: One player is clearly ahead on both growth and sentiment
        if (growth_a > growth_b and sent_a > sent_b) or (growth_b > growth_a and sent_b > sent_a):
            dominant = company_a if (growth_a > growth_b and sent_a > sent_b) else company_b
            follower = company_b if dominant == company_a else company_a
            dom_sent = sent_a if dominant == company_a else sent_b
            dom_growth = growth_a if dominant == company_a else growth_b

            return (
                f"Current signals indicate that {dominant} is outpacing {follower} on both customer sentiment "
                f"(~{dom_sent:.1f}) and growth momentum (~{dom_growth:.1f}). "
                "In practical terms, this combination of traction and goodwill usually translates into stronger pricing power "
                "and better resilience in competitive moves. "
                f"For {follower}, the strategic priority should be to pick one battleground to win first – either closing the experience gap "
                "(sentiment) or creating a sharp, differentiated growth story rather than imitating the leader."
            )

        # Case B: Growth vs sentiment trade-off (one wins growth, other wins sentiment)
        if (growth_a > growth_b and sent_b > sent_a) or (growth_b > growth_a and sent_a > sent_b):
            growth_leader = company_a if growth_a > growth_b else company_b
            sentiment_leader = company_b if growth_leader == company_a else company_a
            g_score = max(growth_a, growth_b)
            s_score = max(sent_a, sent_b)

            return (
                "The data points to a strategic trade-off rather than a clear winner. "
                f"{growth_leader} is winning on growth (~{g_score:.1f}), suggesting stronger near-term deal flow or customer acquisition, while "
                f"{sentiment_leader} leads on sentiment (~{s_score:.1f}), indicating deeper loyalty or better perceived value. "
                "In markets like this, the long-run advantage goes to the player that can import strengths from the other camp – "
                f"either {growth_leader} investing deliberately in experience, or {sentiment_leader} finding a repeatable growth engine."
            )

        # Case C: Metrics are very close – essentially a tie
        if growth_gap < 5 and sentiment_gap < 5:
            return (
                f"On the current evidence, {company_a} and {company_b} are operating in a near-parity zone. "
                "Differences in growth and sentiment sit within what would typically be treated as noise rather than a clear signal. "
                "In this situation, execution details – such as sales discipline, onboarding quality, and partner ecosystem – will matter more than macro positioning. "
                "We would recommend tracking a narrow set of leading indicators (win-rates in key segments, expansion within existing accounts) over the next 2–3 quarters "
                "before making any irreversible strategic bet."
            )

        # Case D: One side looks riskier despite similar growth
        if abs(growth_a - growth_b) < 10 and abs(risk_a - metrics_b.get('risk', 0)) > 0.1:
            riskier = company_a if risk_a > metrics_b.get('risk', 0) else company_b
            steadier = company_b if riskier == company_a else company_a
            return (
                f"While top-line growth looks comparable today, the risk profile is not. {riskier} shows more volatility in the underlying signals, "
                f"whereas {steadier} appears structurally steadier. "
                "In board-level discussions, this typically translates into different appetites: one for optionality and upside, the other for compounding and predictability. "
                f"Capital allocators who are more risk-tolerant may lean towards {riskier}, while conservative operators will likely favour {steadier}."
            )

        # Fallback narrative if none of the above patterns are strong
        return (
            "From a strategic standpoint, the current data does not yet support a simple \"winner-takes-all\" narrative. "
            f"{company_a} is positioned with sentiment around ({sent_a:.1f}) and growth around ({growth_a:.1f}), while "
            f"{company_b} sits at sentiment ({sent_b:.1f}) and growth ({growth_b:.1f}). "
            "In this band, disciplined experimentation – testing specific plays in pricing, packaging, or go-to-market motion – will create more insight "
            "than top-down theorising. We would revisit this view once a clear separation emerges in either sustained growth or durable sentiment."
        )
