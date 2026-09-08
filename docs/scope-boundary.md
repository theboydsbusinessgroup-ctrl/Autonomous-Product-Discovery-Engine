# Scope Boundary

## Product Discovery Engine

This repository is the autonomous digital-product income engine. Its mission is to discover, evaluate, create/source, launch, sell, measure, improve, scale, or retire digital products based on economic evidence.

## Autonomous Media Engine

The autonomous media/content system is a **separate project** and must not be implemented as a subsystem of this repository.

Its separate mission is to operate a daily content-to-cash loop:

**Discover topics → research → generate original engaging content → quality/rights checks → produce platform-specific assets → publish across supported social platforms → monitor performance → collect eligible platform monetization/payouts → learn and optimize → repeat daily.**

The media engine should be independently deployable and should own its own content pipeline, platform adapters, publishing state, analytics, monetization tracking, and operational controls.

## Separation Rule

Do not merge the media engine into this repository. Do not treat media production, social publishing, or platform payout collection as part of the digital-product discovery engine.

Cross-project reporting may occur through JARVIS where explicitly authorized, but project source code, credentials, platform state, and proprietary production records remain isolated.
