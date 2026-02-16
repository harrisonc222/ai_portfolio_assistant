import pandas as pd


def classify_regime(X: pd.DataFrame):
    regime = pd.Series(index=X.index, dtype="object")

    regime[(X["vol_20"] > 0.25) & (X["mom_20"] < 0)] = "RISK_OFF"
    regime[(X["mom_20"] > 0) & (X["vol_20"] < 0.25)] = "RISK_ON"

    regime[regime.isna()] = "NEUTRAL"

    return regime
