from __future__ import annotations

import json
import os

import anthropic
from pydantic import BaseModel

from models import Script, TopicCandidate

# Server-side refusal fallback: if the primary model declines, the API re-runs
# the same request on a fallback model it picks by refusal category.
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class TopicChoice(BaseModel):
    selected_title: str
    reason: str


class MediaAgents:
    """AI decision layer. Platform I/O is deliberately separated from reasoning."""

    def __init__(self) -> None:
        # Reads ANTHROPIC_API_KEY (or an `ant auth login` profile) from the environment.
        self.client = anthropic.Anthropic()
        self.model = os.getenv("CLAUDE_MODEL", "claude-opus-5-5")

    def _parse(self, prompt: str, output_format: type[BaseModel], effort: str) -> BaseModel:
        response = self.client.beta.messages.parse(
            model=self.model,
            max_tokens=16000,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            output_config={"effort": effort},
            output_format=output_format,
            messages=[{"role": "user", "content": prompt}],
        )
        if response.stop_reason == "refusal":
            category = response.stop_details.category if response.stop_details else None
            raise RuntimeError(f"Claude declined the request (category: {category})")
        if response.stop_reason == "max_tokens" or response.parsed_output is None:
            raise RuntimeError(f"Claude returned no usable output (stop_reason: {response.stop_reason})")
        return response.parsed_output

    def choose_topic(self, candidates: list[TopicCandidate]) -> TopicCandidate:
        prompt = {
            "task": "Select the strongest content opportunity. Return its title exactly as given.",
            "rules": [
                "Favor audience value and originality.",
                "Avoid repetitive or mass-produced concepts.",
                "Reject unsupported claims and high rights/copyright risk.",
                "Prefer topics that can produce a strong long-form episode and multiple short derivatives.",
            ],
            "candidates": [c.model_dump() for c in candidates],
        }
        try:
            choice = self._parse(json.dumps(prompt), TopicChoice, effort="medium")
            selected = choice.selected_title.strip().lower()
            for candidate in candidates:
                if candidate.title.strip().lower() == selected:
                    return candidate
            for candidate in candidates:
                if candidate.title.lower() in selected:
                    return candidate
        except RuntimeError:
            pass
        return max(candidates, key=lambda c: c.demand_score + c.originality_score + c.monetization_score)

    def write_script(self, topic: TopicCandidate) -> Script:
        prompt = f"""
Create an original, source-grounded video script for this topic:
{topic.title}

Angle: {topic.angle}
Audience: {topic.audience}

Requirements:
- Strong first 10 seconds.
- Clear narrative progression.
- Useful or entertaining substance throughout.
- No fabricated facts, quotes, statistics, or citations.
- Include source URLs/titles used for factual claims.
- Avoid generic filler and repetitive phrasing.
- The final script must stand on its own and not depend on copied clips.
"""
        return self._parse(prompt, Script, effort="high")
