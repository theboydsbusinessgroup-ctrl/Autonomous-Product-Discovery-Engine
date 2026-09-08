"""Durable state primitives for autonomous media jobs.

The production adapter can map these records to SQLite/Postgres/DynamoDB/etc. The
core engine only depends on explicit states and idempotency keys.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class JobState(str, Enum):
    DISCOVERED = "discovered"
    RESEARCHED = "researched"
    SCRIPTED = "scripted"
    PRODUCED = "produced"
    QUALITY_CHECKED = "quality_checked"
    READY = "ready"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class JobRecord:
    job_id: str
    content_id: str
    state: JobState = JobState.DISCOVERED
    attempt: int = 0
    idempotency_key: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    last_error: str | None = None
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def transition(self, new_state: JobState, error: str | None = None) -> None:
        """Apply a state transition and keep the record audit-friendly."""
        if new_state == JobState.FAILED:
            self.attempt += 1
        self.state = new_state
        self.last_error = error
        self.updated_at = datetime.now(timezone.utc).isoformat()


ALLOWED_TRANSITIONS: dict[JobState, set[JobState]] = {
    JobState.DISCOVERED: {JobState.RESEARCHED, JobState.FAILED, JobState.BLOCKED},
    JobState.RESEARCHED: {JobState.SCRIPTED, JobState.FAILED, JobState.BLOCKED},
    JobState.SCRIPTED: {JobState.PRODUCED, JobState.FAILED, JobState.BLOCKED},
    JobState.PRODUCED: {JobState.QUALITY_CHECKED, JobState.FAILED, JobState.BLOCKED},
    JobState.QUALITY_CHECKED: {JobState.READY, JobState.FAILED, JobState.BLOCKED},
    JobState.READY: {JobState.SCHEDULED, JobState.FAILED, JobState.BLOCKED},
    JobState.SCHEDULED: {JobState.PUBLISHED, JobState.FAILED, JobState.BLOCKED},
    JobState.PUBLISHED: set(),
    JobState.FAILED: {JobState.RESEARCHED, JobState.SCRIPTED, JobState.PRODUCED, JobState.BLOCKED},
    JobState.BLOCKED: set(),
}


def can_transition(current: JobState, target: JobState) -> bool:
    return target in ALLOWED_TRANSITIONS[current]
