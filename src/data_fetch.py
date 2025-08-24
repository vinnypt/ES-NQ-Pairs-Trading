import os
import pandas as pd
import yfinance as yf

def fetch_eq_nq_data(start="2015-01-01", end="2025-01-01", save_path="data/ES_NQ_daily.csv"):
    tickers = ["ES=F", "NQ=F"]
    data = yf.download(tickers, start=start, end=end, interval="1d")
    close_prices = data["Close"]
    close_prices = close_prices.reset_index()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    close_prices.to_csv(save_path, index=False)
    print(f"Data saved to {save_path}")
    return close_prices

if __name__ == "__main__":
    fetch_eq_nq_data()