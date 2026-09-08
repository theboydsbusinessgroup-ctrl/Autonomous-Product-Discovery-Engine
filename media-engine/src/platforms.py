"""Platform-neutral publishing contracts.

Adapters remain intentionally thin: authentication, upload, scheduling, and analytics
are platform-specific; the engine owns the content decision, idempotency, provenance,
and policy gates.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class PublishRequest:
    content_id: str
    file_url: str
    title: str
    description: str = ""
    hashtags: list[str] = field(default_factory=list)
    publish_at: str | None = None
    ai_generated: bool = True
    idempotency_key: str = ""


@dataclass
class PublishResult:
    platform: str
    accepted: bool
    remote_id: str | None = None
    status: str = "pending"
    message: str = ""


class Publisher(Protocol):
    platform: str

    def publish(self, request: PublishRequest) -> PublishResult:
        ...


@dataclass
class Capability:
    platform: str
    enabled: bool
    requires_user_auth: bool = True
    requires_platform_review: bool = False
    public_posting_available: bool = False
    notes: str = ""


CAPABILITIES = {
    "youtube": Capability(
        platform="youtube",
        enabled=True,
        requires_user_auth=True,
        requires_platform_review=True,
        public_posting_available=False,
        notes="YouTube Data API uploads from unverified projects may be restricted to private viewing until audit.",
    ),
    "tiktok": Capability(
        platform="tiktok",
        enabled=True,
        requires_user_auth=True,
        requires_platform_review=True,
        public_posting_available=False,
        notes="Direct Post requires video.publish approval; unaudited clients are restricted to private viewing.",
    ),
    "instagram": Capability(
        platform="instagram",
        enabled=True,
        requires_user_auth=True,
        requires_platform_review=True,
        public_posting_available=False,
        notes="Use official Meta publishing APIs; never fall back to browser automation by default.",
    ),
    "facebook": Capability(
        platform="facebook",
        enabled=True,
        requires_user_auth=True,
        requires_platform_review=True,
        public_posting_available=False,
        notes="Use official Meta publishing APIs and account/page permissions.",
    ),
}


def can_publish_publicly(platform: str, integration_approved: bool) -> bool:
    capability = CAPABILITIES.get(platform)
    if not capability or not capability.enabled:
        return False
    return capability.public_posting_available and integration_approved
