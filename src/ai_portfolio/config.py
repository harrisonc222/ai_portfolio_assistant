from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    repo_root: Path = Path(__file__).resolve().parents[2]
    cache_dir: Path = repo_root / "data" / "cache"

    default_tickers: tuple[str, ...] = ("SPY", "TLT", "GLD")

    vol_windows: tuple[int, ...] = (20, 63)
    mom_windows: tuple[int, ...] = (20, 63)


CFG = Config()
