from ai_portfolio.config import CFG
from ai_portfolio.data.market_data import load_market_data
from ai_portfolio.features.build_features import build_features
from ai_portfolio.regime.gmm_regime import fit_gmm, characterize_states, label_states
import pandas as pd


def main():
    md = load_market_data(
        tickers=CFG.default_tickers,
        start="2015-01-01",
        end="2024-01-01",
        cache_dir=CFG.cache_dir,
    )

    features = build_features(md.prices, md.returns, market="SPY")
    X = features.X

    # Fit GMM
    states, model = fit_gmm(X, n_states=3)

    # Characterize regimes
    summary = characterize_states(X, states)
    labels = label_states(summary)

    regime_series = pd.Series(states, index=X.index)
    regime_named = regime_series.map(labels)

    print("\n=== Regime Characteristics ===")
    print(summary)

    print("\n=== Regime Counts ===")
    print(regime_named.value_counts())

    print("\nLatest Regime:", regime_named.iloc[-1])


if __name__ == "__main__":
    main()
