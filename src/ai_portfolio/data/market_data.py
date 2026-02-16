from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class MarketData:
    prices: pd.DataFrame
    returns: pd.DataFrame


def _normalize_index(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def _extract_price_panel(data: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    """
    yfinance sometimes returns:
      - MultiIndex columns with levels like ['Close','High',...]
      - Sometimes includes 'Adj Close', sometimes not.
    We prefer 'Adj Close' if present, else fall back to 'Close'.
    """
    if isinstance(data.columns, pd.MultiIndex):
        top = data.columns.get_level_values(0)
        if "Adj Close" in top:
            prices = data["Adj Close"].copy()
        elif "Close" in top:
            prices = data["Close"].copy()
        else:
            raise KeyError(f"Neither 'Adj Close' nor 'Close' found in yfinance columns: {set(top)}")
    else:
        # Single-ticker case (flat columns)
        if "Adj Close" in data.columns:
            prices = data[["Adj Close"]].copy()
        elif "Close" in data.columns:
            prices = data[["Close"]].copy()
        else:
            raise KeyError(f"Neither 'Adj Close' nor 'Close' found in yfinance columns: {list(data.columns)}")
        prices.columns = tickers

    return _normalize_index(prices).dropna(how="all")


def get_prices(
    tickers: Iterable[str],
    start: str,
    end: str,
    cache_dir: Path,
    use_cache: bool = True,
) -> pd.DataFrame:
    tickers = [t.upper() for t in tickers]
    cache_dir.mkdir(parents=True, exist_ok=True)

    # include tickers in cache filename to avoid collisions
    tick_str = "_".join(tickers)
    cache_file = cache_dir / f"prices_{tick_str}_{start}_{end}.parquet"

    if use_cache and cache_file.exists():
        return _normalize_index(pd.read_parquet(cache_file))

    # Force a consistent schema from yfinance
    data = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,   # keep raw close; Adj Close may or may not appear
        group_by="column",   # standard multiindex format for multi-ticker
    )

    prices = _extract_price_panel(data, tickers)
    prices.to_parquet(cache_file)
    return prices


def load_market_data(
    tickers: Iterable[str],
    start: str,
    end: str,
    cache_dir: Path,
    use_cache: bool = True,
) -> MarketData:
    prices = get_prices(tickers, start, end, cache_dir, use_cache=use_cache)
    returns = prices.pct_change().dropna(how="all")
    return MarketData(prices=prices, returns=returns)
