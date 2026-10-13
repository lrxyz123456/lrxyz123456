# SEC Financial Analysis Pipeline

An experimental Python project for collecting company financial-statement data from the SEC Company Facts API, transforming it into analysis-ready datasets, computing selected financial ratios, and generating a simple rules-based signal.

## Project structure

- `sec_filings.py` — downloads selected SEC Company Facts fields and exports statement data
- `financial_ratios.py` — loads processed statements and calculates ratios such as revenue growth, net margin, debt-to-assets, and cash runway
- `signal_generator.py` — applies a simple rule-based scoring framework to the latest observations

## Tools

Python, Pandas, Requests

## Run

Run the scripts from this project folder. The original code writes and reads files under `ingestion/data/processed`.

Before using the SEC endpoint, replace the placeholder `User-Agent` value in `sec_filings.py` with an appropriate identifying value.

```bash
python sec_filings.py
python financial_ratios.py
python signal_generator.py
```

## Project note

The Python scripts in this folder are preserved from my original local project. The repository structure, filename organization, and README were added later for presentation on GitHub.

This is an educational analytics project. The generated signal is not investment advice.
