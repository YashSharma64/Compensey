def test_compare_returns_valid_shape(client):
    payload = {"company_a": "Zomato", "company_b": "Swiggy"}
    resp = client.post("/compare", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["winner"] in ("Zomato", "Swiggy")
    for k in (
        "sentiment_score_a",
        "sentiment_score_b",
        "growth_score_a",
        "growth_score_b",
        "risk_score_a",
        "risk_score_b",
    ):
        assert k in data

    assert isinstance(data["explanation"], list)
    assert isinstance(data["shap_insight"], str)
