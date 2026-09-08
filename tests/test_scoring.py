from engine.scoring import score_opportunity


def test_perfect_score_builds():
    scores = {name: 100 for name in [
        "demand", "competition", "price", "margin", "production_difficulty",
        "automation", "evergreen", "trend", "expansion_potential", "ip_risk"
    ]}
    result = score_opportunity(scores)
    assert result.total == 100
    assert result.decision == "build"


def test_low_score_rejects():
    scores = {name: 0 for name in [
        "demand", "competition", "price", "margin", "production_difficulty",
        "automation", "evergreen", "trend", "expansion_potential", "ip_risk"
    ]}
    result = score_opportunity(scores)
    assert result.total == 0
    assert result.decision == "reject"


def test_missing_dimension_fails():
    try:
        score_opportunity({"demand": 100})
    except ValueError as exc:
        assert "Missing score dimensions" in str(exc)
    else:
        raise AssertionError("Expected missing-dimension validation")
