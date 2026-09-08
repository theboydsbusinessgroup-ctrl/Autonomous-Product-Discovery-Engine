from __future__ import annotations

import json
import os
from openai import OpenAI

from models import Script, TopicCandidate


class MediaAgents:
    """AI decision layer. Platform I/O is deliberately separated from reasoning."""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = os.getenv("OPENAI_MODEL", "gpt-5")

    def choose_topic(self, candidates: list[TopicCandidate]) -> TopicCandidate:
        prompt = {
            "task": "Select the strongest content opportunity.",
            "rules": [
                "Favor audience value and originality.",
                "Avoid repetitive or mass-produced concepts.",
                "Reject unsupported claims and high rights/copyright risk.",
                "Prefer topics that can produce a strong long-form episode and multiple short derivatives.",
            ],
            "candidates": [c.model_dump() for c in candidates],
        }
        response = self.client.responses.create(
            model=self.model,
            input=json.dumps(prompt),
        )
        selected_title = response.output_text.strip()
        for candidate in candidates:
            if candidate.title.lower() in selected_title.lower():
                return candidate
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
Return JSON with hook, title_options, body, call_to_action, sources.
"""
        response = self.client.responses.create(model=self.model, input=prompt)
        data = json.loads(response.output_text)
        return Script.model_validate(data)
