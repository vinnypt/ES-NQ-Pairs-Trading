import pandas as pd
import numpy as np

def backtest(input_path="data/ES_NQ_signals.csv"):
    """
    Backtests the pairs trading strategy using generated signals.
    Calculates daily portfolio returns, cumulative returns, and Sharpe ratio.
    """

    df = pd.read_csv(input_path, parse_dates=["Date"])
    df = df.dropna()

    df["ES_Return"] = df["ES=F"].pct_change()
    df["NQ_Return"] = df["NQ=F"].pct_change()

    df["Portfolio_Return"] = df["Signal"] * (df["ES_Return"] - df["NQ_Return"])

    df["Cumulative_Return"] = (1 + df["Portfolio_Return"]).cumprod()

    mean_return = df["Portfolio_Return"].mean()
    std_return = df["Portfolio_Return"].std()
    sharpe = (mean_return / std_return) * np.sqrt(252) if std_return > 0 else 0

    df["Cumulative_Max"] = df["Cumulative_Return"].cummax()
    df["Drawdown"] = df["Cumulative_Return"] / df["Cumulative_Max"] - 1
    max_drawdown = df["Drawdown"].min()

    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Cumulative Return: {df['Cumulative_Return'].iloc[-1]:.2f}x")
    print(f"Max Drawdown: {max_drawdown:.2%}")

    return df

if __name__ == "__main__":
    backtest()

from utils import plot_cumulative_returns, plot_spread_with_signals

df = backtest()
plot_cumulative_returns(df)
plot_spread_with_signals(df)