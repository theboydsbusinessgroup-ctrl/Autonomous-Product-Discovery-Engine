from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShortForm:
    platform: str
    hook: str
    source_start: float
    source_end: float
    caption: str
    call_to_action: str


def build_derivative_plan(hooks: list[dict], platforms: tuple[str, ...] = (
    "youtube_shorts", "instagram_reels", "tiktok", "facebook_reels"
)) -> list[ShortForm]:
    """Create a platform-neutral derivative plan from timestamped highlights.

    Rendering happens elsewhere so the same approved source segment can be formatted
    independently for each platform.
    """
    output: list[ShortForm] = []
    for hook in hooks:
        for platform in platforms:
            output.append(ShortForm(
                platform=platform,
                hook=hook["hook"],
                source_start=float(hook["start"]),
                source_end=float(hook["end"]),
                caption=hook.get("caption", ""),
                call_to_action=hook.get("cta", "Watch the full story."),
            ))
    return output
