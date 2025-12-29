# Portfolio Ingest Specification (Step 2A)

This document defines the authoritative input contract and output guarantees
for the portfolio ingest layer of the AI Portfolio Decision Assistant.

All downstream modules (exposure, regime, risk, action) rely on the guarantees
defined here.

---

## Purpose

The ingest module converts a user-provided **full portfolio snapshot** into a
clean, validated, and interpretable internal representation.

Design principles:
- Deterministic behavior
- Explicit assumptions
- No silent corrections or aggregation
- Clear error messages for invalid inputs

---

## Scope (v1)

This project assumes a **USD-denominated, U.S.-listed portfolio**.

- All tickers must be U.S.-listed (e.g., NYSE, Nasdaq, NYSE Arca)
- Cash is represented explicitly as `CASH` and assumed to be USD
- No currency conversion is performed in v1

International exposure via U.S.-listed ETFs is supported.

---

## Input Format

### File Type
- CSV

### Required Columns
- `ticker` (string)
- `weight` (number)

### Weight Convention
- Weights represent **fractions of total portfolio value**
- The portfolio must be complete: all weights together represent the entire portfolio
- Weights must sum to **1.0 within tolerance**

**Percent-style inputs (e.g., 55 for 55%) are not supported in v1.**

---

## Decimal Precision

- Weights may include up to **3 decimal places** (thousandths)
- Inputs with more than 3 decimal places must raise an error in v1

Examples:
- Valid: `0.250`, `0.033`, `0.007`
- Invalid: `0.3333`

---

## Cash Handling

Cash may be included as a holding using the reserved ticker:

- `CASH`

Interpretation:
- `CASH` represents uninvested USD cash or cash balance in the account
- `CASH` is treated as its own asset class in downstream modules

---

## Cleaning & Validation Rules

### Ticker Cleaning
- Strip leading and trailing whitespace
- Convert to uppercase
- Empty tickers are invalid

### Weight Validation
- Must be numeric
- Must be non-negative
- Must not be NaN or infinite
- Must conform to decimal precision limits

### Duplicate Tickers
- Duplicate tickers are **not allowed** in v1
- Duplicate detection occurs **after ticker cleaning**
- If duplicates are detected, the ingest must raise an error

Rationale:
Each run is intended to be a deliberate, accurate snapshot of the user’s current holdings.
Users should consolidate holdings before submission.

---

## Portfolio Completeness (Sum-to-1 Rule)

- The sum of all weights must equal **1.0 within tolerance**
- Tolerance (v1):  
