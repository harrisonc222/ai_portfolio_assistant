import pandas as pd
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureSet:
    X: pd.DataFrame


def build_features(prices: pd.DataFrame, returns: pd.DataFrame, market: str):
    X = pd.DataFrame(index=returns.index)

    # 1-day returns
    X["ret_1d"] = returns[market]

    # Volatility
    X["vol_20"] = returns[market].rolling(20).std() * np.sqrt(252)
    X["vol_63"] = returns[market].rolling(63).std() * np.sqrt(252)

    # Momentum
    X["mom_20"] = prices[market].pct_change(20)
    X["mom_63"] = prices[market].pct_change(63)

    return FeatureSet(X=X.dropna())
