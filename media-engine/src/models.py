from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ContentType(str, Enum):
    LONG_FORM = "long_form"
    SHORT = "short"
    REEL = "reel"
    TIKTOK = "tiktok"


class TopicCandidate(BaseModel):
    title: str
    angle: str
    audience: str
    demand_score: float = Field(ge=0, le=1)
    competition_score: float = Field(ge=0, le=1)
    monetization_score: float = Field(ge=0, le=1)
    evergreen_score: float = Field(ge=0, le=1)
    originality_score: float = Field(ge=0, le=1)
    risk_score: float = Field(ge=0, le=1)
    evidence: list[str] = []


class Script(BaseModel):
    hook: str
    title_options: list[str]
    body: str
    call_to_action: str
    sources: list[str] = []


class MediaAsset(BaseModel):
    path: str
    kind: str
    source: str
    commercial_rights_confirmed: bool = False
    attribution_required: bool = False


class PublishJob(BaseModel):
    content_id: str
    content_type: ContentType
    title: str
    description: str
    media_path: str
    scheduled_at: datetime | None = None
    platforms: list[str]
    ai_disclosure_required: bool = False


class PerformanceSnapshot(BaseModel):
    content_id: str
    platform: str
    captured_at: datetime
    views: int = 0
    watch_time_seconds: float = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    subscribers_gained: int = 0
    estimated_revenue: float = 0
