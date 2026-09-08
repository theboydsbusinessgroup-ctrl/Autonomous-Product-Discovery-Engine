# Autonomous Media Engine

An autonomous, multi-platform media production system for personal-income content channels.

## Mission

Discover high-potential topics, generate original long-form videos and short-form derivatives, quality-check them, publish to YouTube/Instagram/TikTok/Facebook, collect performance data, and continuously improve the content strategy with minimal owner involvement.

## Design principles

- Personal-income project, not a business-for-sale.
- Owner involvement is an exception path, not part of the normal workflow.
- Original, useful, non-repetitive content is mandatory.
- Never scrape/re-upload other creators' content.
- Rights/provenance are tracked for every media asset.
- Platform-specific packaging is generated separately from the master asset.
- Long-form is the primary source asset; Shorts/Reels are derived from it when appropriate.
- Analytics feed back into topic selection, hooks, pacing, titles, thumbnails, and publishing cadence.

## Planned pipeline

1. Discover
2. Score
3. Research
4. Outline
5. Script
6. Fact/risk review
7. Generate narration
8. Generate/acquire rights-cleared visuals
9. Assemble master video
10. Generate thumbnail/title/description/captions
11. Quality gate
12. Publish/schedule
13. Collect analytics
14. Learn and iterate

## Runtime

The initial implementation uses Python for orchestration and FFmpeg for media assembly. OpenAI is the reasoning/content layer. GitHub Actions is the development/maintenance automation layer; production scheduling should eventually run on a persistent worker or scheduled cloud job rather than depending solely on Actions.

## Credentials

Never commit secrets. Use environment variables or a secret manager for OpenAI, YouTube/Google OAuth, TikTok, Meta, storage, and any optional media-generation providers.
