"""Transparent opportunity scoring for the Autonomous Product Discovery Engine."""

from dataclasses import dataclass
from typing import Mapping

WEIGHTS = {
    "demand": 25,
    "competition": 15,
    "price": 10,
    "margin": 10,
    "production_difficulty": 10,
    "automation": 10,
    "evergreen": 5,
    "trend": 5,
    "expansion_potential": 5,
    "ip_risk": 5,
}

THRESHOLDS = {
    "build": 80,
    "research": 70,
    "hold": 60,
}


@dataclass(frozen=True)
class ScoreResult:
    total: float
    decision: str
    weighted: Mapping[str, float]


def score_opportunity(scores: Mapping[str, float]) -> ScoreResult:
    """Score an opportunity using 0-100 inputs for every weighted dimension.

    All dimensions are deliberately explicit so the model remains auditable.
    """
    missing = set(WEIGHTS) - set(scores)
    if missing:
        raise ValueError(f"Missing score dimensions: {sorted(missing)}")

    invalid = {k: v for k, v in scores.items() if not 0 <= float(v) <= 100}
    if invalid:
        raise ValueError(f"Scores must be between 0 and 100: {invalid}")

    weighted = {
        key: float(scores[key]) * weight / 100 for key, weight in WEIGHTS.items()
    }
    total = round(sum(weighted.values()), 2)

    if total >= THRESHOLDS["build"]:
        decision = "build"
    elif total >= THRESHOLDS["research"]:
        decision = "research"
    elif total >= THRESHOLDS["hold"]:
        decision = "hold"
    else:
        decision = "reject"

    return ScoreResult(total=total, decision=decision, weighted=weighted)
