import numpy as np


def annualized_vol(returns):
    return np.std(returns) * np.sqrt(252)


def max_drawdown(prices):
    roll_max = prices.cummax()
    drawdown = prices / roll_max - 1
    return drawdown.min()
