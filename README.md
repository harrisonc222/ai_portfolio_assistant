# AI Portfolio Decision Assistant

A portfolio-agnostic decision support tool designed to help long-only investors
understand **market regime context**, **portfolio exposures**, **structural risks**,
and **reasonable adjustment options** — without making buy/sell predictions.

## Philosophy

This project is built around a simple decision framework:

**Regime → Exposure → Risk → Action**

The tool does not attempt to predict markets or generate alpha.
Instead, it augments investor judgment by clarifying what a given
portfolio is implicitly exposed to and how it may behave across
different market environments.

## Current Status

Early development — Step 2A (Portfolio ingest & normalization)

## Planned Capabilities

- Portfolio ingest (ETFs & equities)
- Exposure decomposition (asset class, geography, style proxies)
- Market regime classification
- Scenario-based risk awareness
- Action menus (rebalance, protect, maintain, tilt)
- LLM-assisted explanations (guardrailed, non-prescriptive)

## Non-Goals

- No stock picking
- No price targets
- No automated trading
- No performance guarantees
- v1 scope: USD-denominated portfolios with U.S.-listed tickers (international exposure via U.S.-listed ETFs is fine).

## Roadmap

- [x] Project specification
- [ ] Portfolio ingest & normalization
- [ ] Exposure engine
- [ ] Regime classification
- [ ] Risk scenario engine
- [ ] AI narrative layer
- [ ] Demo interface (CLI / web)
