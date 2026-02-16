import pandas as pd
import numpy as np
from ai_portfolio.regime.threshold_regime import classify_regime


def test_regime_labels():
    idx = pd.date_range("2020-01-01", periods=100, freq="B")
    X = pd.DataFrame({
        "vol_20": np.random.rand(100),
        "mom_20": np.random.randn(100),
    }, index=idx)

    regimes = classify_regime(X)
    assert len(regimes) == 100
