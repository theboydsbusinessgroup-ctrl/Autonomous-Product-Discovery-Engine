# Autonomous Product Discovery Engine

An evidence-driven system for discovering, scoring, validating, creating, launching, and optimizing digital products with minimal owner involvement.

## Mission

Build a repeatable autonomous income engine that:

1. Continuously discovers product opportunities across marketplaces and public demand signals.
2. Scores opportunities using a transparent economic and risk model.
3. Rejects weak, saturated, risky, or poorly automatable ideas.
4. Prefers original products with clean intellectual-property ownership.
5. Builds the smallest viable product before expanding it.
6. Measures real marketplace performance and reallocates effort toward winners.
7. Minimizes ongoing owner involvement and preserves transferability for a future sale.

## Operating principles

- Evidence over intuition.
- Net economics over vanity metrics.
- Original creation over uncertain resale rights.
- Marketplace distribution before audience-building.
- Automation by default; human escalation only when required.
- Seasonal demand should be anticipated, not merely reacted to.
- A niche may be abandoned when the economics stop working.
- Never publish, spend material advertising money, or make legal/IP claims without the required authorization or verified evidence.

## Architecture

- `engine/discovery/` — research adapters and demand-signal collection.
- `engine/scoring/` — opportunity scoring and decision thresholds.
- `engine/validation/` — evidence quality, economics, competition, and IP-risk checks.
- `engine/product_factory/` — product specifications and production orchestration.
- `engine/marketplace/` — marketplace-specific listing and launch abstractions.
- `engine/analytics/` — performance metrics and unit economics.
- `engine/portfolio/` — winner expansion, experimentation, retirement, and capital allocation.
- `opportunities/` — machine-readable opportunity records.
- `products/` — product specifications and build artifacts.
- `research/` — dated research snapshots and evidence.
- `decisions/` — durable decision records.
- `automation/` — scheduled workflows and operational instructions.
- `docs/` — architecture, operating policy, and sale-readiness documentation.
- `tests/` — automated tests.

## Score model

| Dimension | Weight |
|---|---:|
| Demand | 25% |
| Competition | 15% |
| Price | 10% |
| Margin | 10% |
| Production Difficulty | 10% |
| Automation | 10% |
| Evergreen | 5% |
| Trend | 5% |
| Expansion Potential | 5% |
| IP Risk | 5% |

Decision thresholds:

- **80–100:** Build immediately.
- **70–79:** Research further.
- **60–69:** Hold.
- **Below 60:** Reject.

## Current status

**Phase 1 — Foundation:** initialized.

The next implementation stages are discovery adapters, evidence normalization, opportunity scoring, validation, product specifications, and automated evaluation workflows.

## Repository boundary

This repository is intentionally separate from Boyd’s Bar and EventMatch. Do not place their proprietary code, credentials, customer data, or production records here.
