from __future__ import annotations

import sys

from .ingest import IngestError, ingest_portfolio_csv


def print_usage() -> None:
    print(
        "Usage:\n"
        "  python3 -m ai_portfolio.cli ingest <path_to_csv>\n\n"
        "Example:\n"
        "  PYTHONPATH=src python3 -m ai_portfolio.cli ingest data/test.csv"
    )


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]  # skip the script/module name

    if len(argv) == 0:
        print_usage()
        return 2

    cmd = argv[0]

    if cmd == "ingest":
        if len(argv) != 2:
            print_usage()
            return 2

        path = argv[1]
        try:
            portfolio = ingest_portfolio_csv(path)
        except IngestError as e:
            print(f"IngestError: {e}")
            return 1

        print(portfolio)
        return 0

    print(f"Unknown command: {cmd!r}\n")
    print_usage()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
