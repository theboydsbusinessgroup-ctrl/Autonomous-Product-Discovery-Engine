from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from models import TopicCandidate


@dataclass(frozen=True)
class DiscoverySignal:
    title: str
    angle: str
    audience: str
    demand: float
    competition: float
    monetization: float
    evergreen: float
    originality: float
    risk: float
    evidence: tuple[str, ...] = ()


def score_signal(signal: DiscoverySignal) -> TopicCandidate:
    # Weighted toward demand and monetization, while strongly penalizing risk and weak originality.
    score = (
        0.25 * signal.demand
        + 0.20 * (1.0 - signal.competition)
        + 0.20 * signal.monetization
        + 0.15 * signal.evergreen
        + 0.20 * signal.originality
        - 0.20 * signal.risk
    )
    # Discovery score is stored implicitly through component scores; downstream agents
    # should preserve the components so we can explain why a topic was selected.
    _ = score
    return TopicCandidate(
        title=signal.title,
        angle=signal.angle,
        audience=signal.audience,
        demand_score=signal.demand,
        competition_score=signal.competition,
        monetization_score=signal.monetization,
        evergreen_score=signal.evergreen,
        originality_score=signal.originality,
        risk_score=signal.risk,
        evidence=list(signal.evidence),
    )


def rank_signals(signals: Iterable[DiscoverySignal]) -> list[TopicCandidate]:
    candidates = [score_signal(s) for s in signals]
    return sorted(
        candidates,
        key=lambda c: (
            0.25 * c.demand_score
            + 0.20 * (1 - c.competition_score)
            + 0.20 * c.monetization_score
            + 0.15 * c.evergreen_score
            + 0.20 * c.originality_score
            - 0.20 * c.risk_score
        ),
        reverse=True,
    )
