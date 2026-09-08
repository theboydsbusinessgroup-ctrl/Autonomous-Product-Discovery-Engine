from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QualityResult:
    approved: bool
    quality_score: float
    originality_score: float
    rights_confidence: float
    reasons: list[str]


def evaluate(*, quality_score: float, originality_score: float, rights_confidence: float,
             minimum_quality: float = 0.82, minimum_originality: float = 0.90,
             minimum_rights: float = 0.98) -> QualityResult:
    reasons: list[str] = []
    if quality_score < minimum_quality:
        reasons.append("quality_below_threshold")
    if originality_score < minimum_originality:
        reasons.append("originality_below_threshold")
    if rights_confidence < minimum_rights:
        reasons.append("rights_confidence_below_threshold")
    return QualityResult(
        approved=not reasons,
        quality_score=quality_score,
        originality_score=originality_score,
        rights_confidence=rights_confidence,
        reasons=reasons,
    )
