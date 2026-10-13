import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
import os 

ticker_s = input("ticker symbol (default = KO) : ").upper().strip()
if not ticker_s:
    ticker_s = "KO"

dat = yf.Ticker(ticker_s)
dividend = dat.dividends

if dividend.empty:
    print("No dividend history found for this ticker.")
    exit()

div_df = dividend.reset_index()
div_df.columns = ["Ex-Date", "Dividend"]
div_df = div_df.tail()

#Stock Prices Before&After Ex-Dividend Dates
div_df["Ex-Date"] = pd.to_datetime(div_df["Ex-Date"])
ex_date = div_df["Ex-Date"].max()
print("Ex-Dividend Date : ", ex_date.date())

start_date = ex_date - timedelta(days=3)
end_date = ex_date + timedelta(days=3)

price_df = dat.history(start = start_date, end = end_date)

plt.figure(figsize=(10,5))
plt.plot(price_df.index, price_df["Close"], marker="o")
plt.axvline(ex_date, linestyle="--", label="Ex-Dividend Date")
plt.title(f"{ticker_s} price around ex-dividend date")
plt.xlabel("Date")
plt.ylabel("Stock Price ($)")
plt.legend()
plt.grid(True)



plt.figure(figsize=(10,5))
plt.bar(div_df["Ex-Date"], div_df["Dividend"], color='skyblue', width=20)
plt.xlabel("Ex-Dividend Date")
plt.ylabel("Dividend Amount ($)")
plt.title(f"Dividends of {ticker_s} Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

csv_file = f"{ticker_s}_dividends.csv"
div_df.to_csv(csv_file, index=False)
print(f"\nDividend data saved to {csv_file}")