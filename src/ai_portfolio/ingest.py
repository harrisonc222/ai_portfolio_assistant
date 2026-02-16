from __future__ import annotations
from decimal import Decimal, InvalidOperation
import csv
from decimal import Decimal
from typing import List, Tuple


## Look in same package and find models.py
from .models import Portfolio, Holding

class IngestError(ValueError):
    """Raised when portfolio input violates the Step 2A ingest specification."""

def clean_ticker(raw: str) -> str:
    """
    Clean a ticker according to the spec:
    - strip whitespace
    - uppercase
    - non-empty
    """
    t = (raw or "").strip().upper()
    if not t:
          raise IngestError("Empty ticker is not allowed.")
    return t

def parse_weight(raw: str) -> Decimal:
    """
    Parse and validate a weight according to the spec:
    - must be numeric
    - must be non-negative
    - must have <= 3 decimal places
    Returns a Decimal for exact precision handling.
    """
    s = str(raw).strip()
    try:
        w = Decimal(s)
    except (InvalidOperation, ValueError) as e:
        raise IngestError(f"Invalid weight value: {raw!r}") from e

    if w.is_nan() or w.is_infinite():
        raise IngestError(f"Weight must be a finite number: {raw!r}")

    if w < 0:
        raise IngestError(f"Negative weights are not allowed: {w}")

    # Enforce <= 3 decimal places (thousandths)
    if w.as_tuple().exponent < -3:
        raise IngestError(f"Weight {w} exceeds maximum precision (3 decimal places).")

    return w

def read_holdings_csv(path: str) -> list[tuple[str, Decimal]]:
    """
    Read a CSV with headers: ticker,weight
    Returns list of (ticker, weight).
    Raises IngestError with line numbers on bad inputs.
    """
    rows: list[tuple[str, Decimal]] = []

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise IngestError("CSV has no header row.")

            headers = {h.strip().lower() for h in reader.fieldnames if h}
            if "ticker" not in headers or "weight" not in headers:
                raise IngestError("CSV must contain headers: ticker,weight")

            for line_no, r in enumerate(reader, start=2):  # header is line 1
                try:
                    ticker = clean_ticker(r.get("ticker", ""))
                    weight = parse_weight(r.get("weight", ""))
                except IngestError as e:
                    raise IngestError(f"Line {line_no}: {e}") from e

                rows.append((ticker, weight))

    except FileNotFoundError as e:
        raise IngestError(f"File not found: {path}") from e
    
    if not rows:
        raise IngestError("No holdings found in CSV.")

    return rows

def validate_no_duplicates(rows: list[tuple[str, Decimal]]) -> None:
    """Reject duplicate tickers (after cleaning), per spec."""
    seen: set[str] = set()
    for ticker, _ in rows:
        if ticker in seen:
            raise IngestError(f"Duplicate ticker detected: {ticker}")
        seen.add(ticker)

def validate_sum_to_one(rows: list[tuple[str, Decimal]], tolerance: Decimal = Decimal("0.001")) -> None:
    """Enforce weights sum to 1.0 within tolerance."""
    total = sum((w for _, w in rows), start=Decimal("0"))

    if abs(total - Decimal("1.0")) > tolerance:
        raise IngestError(f"Weights sum to {total}, expected 1.0 (±{tolerance}).")

def build_portfolio(rows: list[tuple[str, Decimal]]) -> Portfolio:
    """
    Convert validated (ticker, Decimal weight) rows into a Portfolio.
    Deterministic output: sorted by ticker.
    """
    rows_sorted = sorted(rows, key=lambda x: x[0])
    holdings = []
    for t, w in rows_sorted:
        holding = Holding(ticker=t, weight=float(w))
        holdings.append(holding)

    return Portfolio(holdings=holdings)

def ingest_portfolio_csv(path: str) -> Portfolio:
    """
    Main Step 2A entry point:
    - read CSV
    - validate rules
    - return Portfolio object
    """
    rows = read_holdings_csv(path)
    validate_no_duplicates(rows)
    validate_sum_to_one(rows)
    return build_portfolio(rows)

