import pandas as pd
import numpy as np

def backtest(input_path="data/ES_NQ_signals.csv"):
    """
    Backtests the pairs trading strategy using generated signals.
    Calculates daily portfolio returns, cumulative returns, and Sharpe ratio.
    Returns the DataFrame and key metrics.
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

    trade_mask = df["Signal"].shift(1) != 0 
    trade_returns = df.loc[trade_mask, "Portfolio_Return"]
    hit_rate = (trade_returns > 0).sum() / len(trade_returns) if len(trade_returns) > 0 else np.nan

    metrics = {
        "sharpe": sharpe,
        "cumulative_return": df["Cumulative_Return"].iloc[-1],
        "max_drawdown": max_drawdown,
        "hit_rate": hit_rate
    }

    return df, metrics

df = backtest()

if __name__ == "__main__":
    from utils import plot_cumulative_returns, plot_spread_with_signals
    df, metrics = backtest()
    print(f"Sharpe Ratio: {metrics['sharpe']:.2f}")
    print(f"Cumulative Return: {metrics['cumulative_return']:.2f}x")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"Hit Rate: {metrics['hit_rate']:.2%}")
    plot_cumulative_returns(df)
    plot_spread_with_signals(df)