"""Source-grounded research planning and claim ledger for the autonomous media engine.

This module deliberately separates research from generation. It creates a structured
research packet that can be persisted, audited, and passed to the script agent.
Network fetching is injected so production can use approved search/connectors without
coupling the core research logic to one provider.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Iterable, Sequence
from urllib.parse import urlparse


@dataclass
class Source:
    url: str
    title: str
    publisher: str = ""
    reliability: float = 0.0
    published_at: str | None = None
    retrieved_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = ""

    def valid_url(self) -> bool:
        parsed = urlparse(self.url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


@dataclass
class Claim:
    text: str
    source_urls: list[str] = field(default_factory=list)
    confidence: float = 0.0
    status: str = "unverified"  # unverified | supported | disputed | rejected
    notes: str = ""


@dataclass
class ResearchPacket:
    topic: str
    angle: str
    sources: list[Source]
    claims: list[Claim]
    open_questions: list[str] = field(default_factory=list)
    research_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def source_urls(self) -> list[str]:
        return [source.url for source in self.sources]

    @property
    def support_rate(self) -> float:
        if not self.claims:
            return 0.0
        supported = sum(claim.status == "supported" for claim in self.claims)
        return supported / len(self.claims)


def validate_sources(sources: Iterable[Source], minimum_reliability: float = 0.70) -> list[Source]:
    """Return sources that are valid URLs and meet the reliability floor."""
    return [
        source
        for source in sources
        if source.valid_url() and source.reliability >= minimum_reliability
    ]


def build_claim_ledger(claims: Sequence[Claim], sources: Sequence[Source]) -> list[Claim]:
    """Attach only known source URLs and conservatively classify unsupported claims."""
    known_urls = {source.url for source in sources}
    ledger: list[Claim] = []
    for claim in claims:
        linked = [url for url in claim.source_urls if url in known_urls]
        status = claim.status
        if not linked and status == "supported":
            status = "unverified"
        ledger.append(
            Claim(
                text=claim.text.strip(),
                source_urls=linked,
                confidence=max(0.0, min(1.0, claim.confidence)),
                status=status,
                notes=claim.notes,
            )
        )
    return ledger


def research_topic(
    topic: str,
    angle: str,
    source_finder: Callable[[str], Iterable[Source]],
    claim_extractor: Callable[[str, Sequence[Source]], Iterable[Claim]],
    minimum_sources: int = 3,
) -> ResearchPacket:
    """Build an auditable research packet using injected discovery/extraction functions."""
    raw_sources = list(source_finder(topic))
    sources = validate_sources(raw_sources)
    # Prefer diverse publishers while preserving the best reliability score.
    unique: dict[str, Source] = {}
    for source in sorted(sources, key=lambda item: item.reliability, reverse=True):
        unique.setdefault(source.url, source)
    sources = list(unique.values())

    claims = build_claim_ledger(claim_extractor(topic, sources), sources)
    open_questions = [
        f"Insufficient independent sources: found {len(sources)}, need at least {minimum_sources}."
    ] if len(sources) < minimum_sources else []

    return ResearchPacket(
        topic=topic,
        angle=angle,
        sources=sources,
        claims=claims,
        open_questions=open_questions,
    )


def research_is_publishable(packet: ResearchPacket, minimum_sources: int = 3) -> bool:
    """Conservative publish gate for source-grounded factual content."""
    if len(packet.sources) < minimum_sources:
        return False
    if not packet.claims:
        return False
    return all(
        claim.status == "supported" and claim.source_urls and claim.confidence >= 0.80
        for claim in packet.claims
    )
