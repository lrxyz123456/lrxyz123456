from datetime import timedelta

import pandas as pd
import yfinance as yf


def build_dividend_window_dataset(
    tickers,
    start_date="2023-01-01",
    before_window=5,
    after_window=5,
):
    start_date = pd.Timestamp(start_date, tz="UTC")
    rows = []

    for ticker_symbol in tickers:
        ticker = yf.Ticker(ticker_symbol)
        dividends = ticker.dividends

        for ex_date, dividend_amount in dividends.items():
            if ex_date < start_date:
                continue

            price_window = ticker.history(
                start=ex_date - timedelta(days=before_window + 10),
                end=ex_date + timedelta(days=after_window + 10),
            )["Close"]

            try:
                ex_index = price_window.index.get_loc(ex_date)
                price_before = price_window.iloc[ex_index - before_window]
                price_after = price_window.iloc[ex_index + after_window]
            except (KeyError, IndexError):
                continue

            annual_dividend = dividend_amount * 4
            dividend_yield = (annual_dividend / price_before) * 100
            price_change = price_after - price_before
            percent_change = (price_change / price_before) * 100

            rows.append(
                {
                    "Ticker": ticker_symbol,
                    "Ex-Dividend Date": ex_date,
                    "Dividend ($)": round(dividend_amount, 3),
                    "Price Before": round(price_before, 3),
                    "Price After": round(price_after, 3),
                    "Price Change ($)": round(price_change, 3),
                    "Price Change (%)": round(percent_change, 3),
                    "Annual Dividend ($)": round(annual_dividend, 3),
                    "Dividend Yield (%)": round(dividend_yield, 3),
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    dataset = build_dividend_window_dataset(["JNJ"])
    dataset.to_csv("dividend_windows.csv", index=False)
    print(dataset)
