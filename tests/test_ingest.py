import pytest

from ai_portfolio.ingest import IngestError, ingest_portfolio_csv


def write_csv(tmp_path, name: str, text: str) -> str:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_ingest_happy_path(tmp_path):
    path = write_csv(
        tmp_path,
        "ok.csv",
        "ticker,weight\n"
        "VTI,0.450\n"
        "VXUS,0.200\n"
        "QQQ,0.200\n"
        "CASH,0.150\n",
    )
    portfolio = ingest_portfolio_csv(path)

    assert [h.ticker for h in portfolio.holdings] == ["CASH", "QQQ", "VTI", "VXUS"]
    assert abs(sum(h.weight for h in portfolio.holdings) - 1.0) < 1e-9


def test_reject_duplicate_ticker(tmp_path):
    path = write_csv(
        tmp_path,
        "dup.csv",
        "ticker,weight\n"
        "VTI,0.500\n"
        "VTI,0.200\n"
        "CASH,0.300\n",
    )
    with pytest.raises(IngestError, match="Duplicate ticker"):
        ingest_portfolio_csv(path)


def test_reject_sum_not_one(tmp_path):
    path = write_csv(
        tmp_path,
        "bad_sum.csv",
        "ticker,weight\n"
        "VTI,0.500\n"
        "QQQ,0.400\n"
        "CASH,0.050\n",
    )
    with pytest.raises(IngestError, match="Weights sum to"):
        ingest_portfolio_csv(path)


def test_reject_empty_ticker(tmp_path):
    path = write_csv(
        tmp_path,
        "empty_ticker.csv",
        "ticker,weight\n"
        ",0.500\n"
        "CASH,0.500\n",
    )
    with pytest.raises(IngestError, match="Empty ticker"):
        ingest_portfolio_csv(path)


def test_reject_negative_weight(tmp_path):
    path = write_csv(
        tmp_path,
        "neg.csv",
        "ticker,weight\n"
        "VTI,-0.100\n"
        "CASH,1.100\n",
    )
    with pytest.raises(IngestError, match="Negative weights"):
        ingest_portfolio_csv(path)


def test_reject_more_than_3_decimals(tmp_path):
    path = write_csv(
        tmp_path,
        "precision.csv",
        "ticker,weight\n"
        "VTI,0.1255\n"
        "CASH,0.8745\n",
    )
    with pytest.raises(IngestError, match="exceeds maximum precision"):
        ingest_portfolio_csv(path)


def test_reject_4_decimal_places_even_if_trailing_zero(tmp_path):
    # strict rule: max 3 decimal places as typed
    path = write_csv(
        tmp_path,
        "trailing_zero.csv",
        "ticker,weight\n"
        "VTI,0.1250\n"
        "CASH,0.8750\n",
    )
    with pytest.raises(IngestError, match="exceeds maximum precision"):
        ingest_portfolio_csv(path)
