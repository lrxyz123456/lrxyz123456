import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt

start_date = pd.Timestamp(2023, 1, 1, tz="UTC")

before_ex_div_window = 5
after_ex_div_window = 5

all_rows = []

list_of_tickers = [
    "JNJ"
]

for ticker in list_of_tickers:
    dat = yf.Ticker(ticker)
    dividend_series = dat.dividends

    for ex_date, dividend_amount in dividend_series.items():
        if ex_date >= start_date:
            price_window = dat.history(
                start=ex_date - timedelta(days=before_ex_div_window + 10),
                end=ex_date + timedelta(days=after_ex_div_window + 10)
            )["Close"]

            try:
                ex_idx = price_window.index.get_loc(ex_date)
            except KeyError:
                continue
            
            price_before = price_window.iloc[ex_idx - before_ex_div_window]
            price_after = price_window.iloc[ex_idx + after_ex_div_window]

            annual_dividend = dividend_amount * 4 
            dividend_yield = (annual_dividend / price_before) * 100

            price_change = price_after - price_before
            percent_change = (price_change / price_before) * 100

            row = {
                "Ticker": ticker,
                "Ex-Dividend Date": ex_date,
                "Dividend ($)": round(dividend_amount, 3),

                "Price Before": round(price_before, 3),
                "Price After": round(price_after, 3),

                "Price Change ($)": round(price_change, 3),
                "Price Change (%)": round(percent_change, 3),

                "Annual Dividend ($)": round(annual_dividend, 3),
                "Dividend Yield (%)": round(dividend_yield, 3)
            }

            all_rows.append(row)

df = pd.DataFrame(all_rows)
df.to_csv("dividend_windows.csv", index=False)