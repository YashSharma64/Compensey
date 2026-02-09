def test_strategy_returns_memo(client):
    payload = {
        "company_a": "Zomato",
        "company_b": "Swiggy",
        "metrics_a": {"sentiment": 85.0, "growth": 72.3, "risk": 0.18},
        "metrics_b": {"sentiment": 78.0, "growth": 68.5, "risk": 0.24},
        "question": "Who will win in the long term and what should the laggard do next?",
    }
    resp = client.post("/strategy", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert "Recommendation:" in data["answer"]


def test_strategy_includes_drivers_when_provided(client):
    payload = {
        "company_a": "Zomato",
        "company_b": "Swiggy",
        "metrics_a": {"sentiment": 85.0, "growth": 72.3, "risk": 0.18},
        "metrics_b": {"sentiment": 78.0, "growth": 68.5, "risk": 0.24},
        "question": "What should we do next?",
        "drivers": ["Higher 4–5 star share", "Shorter review length implies clearer feedback"],
    }
    resp = client.post("/strategy", json=payload)
    assert resp.status_code == 200

    memo = resp.json()["answer"]
    assert "Drivers:" in memo
