import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture


def fit_gmm(X: pd.DataFrame, n_states: int = 3):
    model = GaussianMixture(
        n_components=n_states,
        covariance_type="full",
        random_state=42
    )
    model.fit(X)
    states = model.predict(X)

    return states, model


def characterize_states(X: pd.DataFrame, states: np.ndarray):
    df = X.copy()
    df["state"] = states

    summary = (
        df.groupby("state")
        .agg(
            avg_return=("ret_1d", "mean"),
            avg_vol=("vol_20", "mean")
        )
        .sort_values("avg_vol")
    )

    return summary


def label_states(summary: pd.DataFrame):
    """
    Automatically label:
      - Highest vol state → RISK_OFF
      - Lowest vol & positive return → RISK_ON
      - Everything else → NEUTRAL
    """
    labels = {}

    # Highest vol
    risk_off_state = summary["avg_vol"].idxmax()
    labels[risk_off_state] = "RISK_OFF"

    # Lowest vol with positive return
    sorted_states = summary.sort_values("avg_vol").index.tolist()

    for s in sorted_states:
        if s not in labels:
            if summary.loc[s, "avg_return"] > 0:
                labels[s] = "RISK_ON"
                break

    # Remaining
    for s in summary.index:
        if s not in labels:
            labels[s] = "NEUTRAL"

    return labels
