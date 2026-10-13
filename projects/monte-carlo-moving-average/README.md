# Monte Carlo Moving-Average Strategy Simulation

A Python project that simulates synthetic asset-price paths and tests a simple moving-average trading rule across repeated Monte Carlo runs.

## What it does

- Generates price paths using Gaussian daily returns
- Applies a moving-average buy/sell rule
- Tracks trade profit and loss
- Repeats the strategy across many simulations
- Visualizes simulated paths, example trades, and the PnL distribution

## Tools

Python, Matplotlib, `random`, `collections.deque`

## Run

```bash
python monte_carlo_strategy.py
```

This is an educational simulation project, not investment advice.
