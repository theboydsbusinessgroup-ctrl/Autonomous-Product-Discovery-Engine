from __future__ import annotations

from agents import MediaAgents
from models import TopicCandidate


def run_candidate_pipeline(candidates: list[TopicCandidate]) -> dict:
    agents = MediaAgents()
    topic = agents.choose_topic(candidates)
    script = agents.write_script(topic)

    # Rendering, rights validation, platform adapters, and analytics are intentionally
    # separate modules. This prevents a publishing failure from corrupting content state.
    return {
        "topic": topic.model_dump(),
        "script": script.model_dump(),
        "next": [
            "rights_gate",
            "voice_generation",
            "visual_generation",
            "ffmpeg_render",
            "quality_gate",
            "platform_publish",
            "analytics_feedback",
        ],
    }
