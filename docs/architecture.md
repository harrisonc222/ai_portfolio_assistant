# System Architecture (High Level)

The system is structured as a modular decision-support pipeline:

1. **Portfolio Ingest**
   - Accepts user holdings and constraints via command line
   - Normalizes and validates inputs
   - inputs consist of weights, tickers, price.

2. **Exposure Analysis**
   - Translates holdings into economic and risk exposures

3. **Regime Classification**
   - Classifies the current macro-financial environment

4. **Risk Awareness**
   - Identifies scenarios and conditions that historically stress the portfolio

5. **Decision Menu**
   - Presents reasonable adjustment options without prescriptive advice

6. **Narrative Layer**
   - Uses an LLM to explain results in plain language

Each layer is designed to be interpretable, deterministic where possible,
and extensible.
