# SEC Financial Analysis Pipeline

An experimental Python project for collecting company financial-statement data from the SEC Company Facts API, transforming it into analysis-ready datasets, computing selected financial ratios, and generating a simple rules-based signal.

## Project structure

- `sec_filings.py` — downloads selected SEC Company Facts fields and exports statement data
- `financial_ratios.py` — loads processed statements and calculates ratios such as revenue growth, net margin, debt-to-assets, and cash runway
- `signal_generator.py` — applies a simple rule-based scoring framework to the latest observations

## Tools

Python, Pandas, Requests

## Notes

The SEC requires a descriptive `User-Agent` header. Set the `SEC_USER_AGENT` environment variable before making requests.

```bash
export SEC_USER_AGENT="Your Name your.email@example.com"
python sec_filings.py
python financial_ratios.py
python signal_generator.py
```

This is an educational analytics project. The generated signal is not investment advice.
