from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


def analyze_ticker(ticker_symbol="KO"):
    ticker = yf.Ticker(ticker_symbol)
    dividends = ticker.dividends

    if dividends.empty:
        raise ValueError(f"No dividend history found for {ticker_symbol}.")

    dividend_df = dividends.reset_index()
    dividend_df.columns = ["Ex-Date", "Dividend"]
    dividend_df = dividend_df.tail()
    dividend_df["Ex-Date"] = pd.to_datetime(dividend_df["Ex-Date"])

    ex_date = dividend_df["Ex-Date"].max()
    start_date = ex_date - timedelta(days=3)
    end_date = ex_date + timedelta(days=3)

    price_df = ticker.history(start=start_date, end=end_date)

    plt.figure(figsize=(10, 5))
    plt.plot(price_df.index, price_df["Close"], marker="o")
    plt.axvline(ex_date, linestyle="--", label="Ex-Dividend Date")
    plt.title(f"{ticker_symbol} Price Around Ex-Dividend Date")
    plt.xlabel("Date")
    plt.ylabel("Stock Price ($)")
    plt.legend()
    plt.grid(True)

    plt.figure(figsize=(10, 5))
    plt.bar(dividend_df["Ex-Date"], dividend_df["Dividend"], width=20)
    plt.xlabel("Ex-Dividend Date")
    plt.ylabel("Dividend Amount ($)")
    plt.title(f"Recent Dividends of {ticker_symbol}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    csv_file = f"{ticker_symbol}_dividends.csv"
    dividend_df.to_csv(csv_file, index=False)
    print(f"Dividend data saved to {csv_file}")


if __name__ == "__main__":
    ticker_input = input("Ticker symbol (default = KO): ").upper().strip() or "KO"
    analyze_ticker(ticker_input)
