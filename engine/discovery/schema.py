"""Normalized evidence records used by discovery adapters."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class Evidence:
    source: str
    url: str
    observed_at: str
    signal: str
    value: str
    confidence: float = 0.5
    metadata: dict[str, str] = field(default_factory=dict)

    @classmethod
    def now(
        cls,
        *,
        source: str,
        url: str,
        signal: str,
        value: str,
        confidence: float = 0.5,
        metadata: dict[str, str] | None = None,
    ) -> "Evidence":
        return cls(
            source=source,
            url=url,
            observed_at=datetime.now(timezone.utc).isoformat(),
            signal=signal,
            value=value,
            confidence=confidence,
            metadata=metadata or {},
        )
