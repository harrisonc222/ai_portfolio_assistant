import pandas as pd
import numpy as np
from ai_portfolio.features.build_features import build_features


def test_feature_generation():
    idx = pd.date_range("2020-01-01", periods=300, freq="B")
    prices = pd.DataFrame({"SPY": 100 + np.cumsum(np.random.randn(len(idx)))}, index=idx)
    returns = prices.pct_change().dropna()

    fs = build_features(prices, returns, market="SPY")

    assert not fs.X.isna().any().any()
    assert len(fs.X.columns) > 0
