import pandas as pd
import matplotlib.pyplot as plt

def plot_cumulative_returns(df, title="Cumulative Returns"):
    """
    Plots the cumulative returns of the strategy.
    Expects a DataFrame with 'Date' and 'Cumulative_Return'.
    """
    plt.figure(figsize=(10,5))
    plt.plot(df["Date"], df["Cumulative_Return"], label="Strategy")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (x)")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_spread_with_signals(df, title="Spread with Trading Signals"):
    """
    Plots the spread and highlights buy/sell signals.
    Expects DataFrame with 'Date', 'Spread', and 'Signal'.
    """
    plt.figure(figsize=(12,6))
    plt.plot(df["Date"], df["Spread"], label="Spread", color="blue")

    buys = df[df["Signal"] == 1]
    plt.scatter(buys["Date"], buys["Spread"], color="green", label="Long ES / Short NQ", marker="^", alpha=0.8)