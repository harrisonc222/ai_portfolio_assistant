from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Holding:
    """
    Represents a single portfolio holding.

    Attributes
    ----------
    ticker : str
        Cleaned, uppercase ticker symbol (e.g. 'VTI', 'QQQ', 'CASH').
    weight : float
        Fraction of total portfolio value.
    """
    ticker: str
    weight: float


@dataclass(frozen=True)
class Portfolio:
    """
    Represents a full portfolio snapshot.

    Attributes
    ----------
    holdings : List[Holding]
        List of portfolio holdings.
    """
    holdings: List[Holding]
