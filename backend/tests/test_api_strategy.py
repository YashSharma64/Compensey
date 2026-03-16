import pytest
from unittest.mock import patch

@patch("google.generativeai.GenerativeModel.generate_content")
def test_strategy_returns_memo(mock_generate, client):
    class MockResponse:
        text = "Recommendation: Based on the metrics, Zomato is positioned for long-term outperformance."

    mock_generate.return_value = MockResponse()

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


@patch("google.generativeai.GenerativeModel.generate_content")
def test_strategy_includes_drivers_when_provided(mock_generate, client):
    class MockResponse:
        text = "Drivers: Higher 4-5 star share. Recommendation: Maintain current trajectory."

    mock_generate.return_value = MockResponse()

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

