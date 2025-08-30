import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

def calculate_spread(input_path="data/ES_NQ_daily.csv", output_path="data/ES_NQ_spread.csv"):
    df = pd.read_csv(input_path, parse_dates=["Date"])
    df = df.dropna()
    window = 40
    hedge_ratios = []
    spreads = []
    for i in range(len(df)):
        if i < window:
            hedge_ratios.append(float('nan'))
            spreads.append(float('nan'))
            continue
        es_window = df["ES=F"].iloc[i-window+1:i+1]
        nq_window = df["NQ=F"].iloc[i-window+1:i+1]
        nq_const = sm.add_constant(nq_window)
        model = sm.OLS(es_window, nq_const).fit()
        hedge_ratio = model.params["NQ=F"]
        spread = df["ES=F"].iloc[i] - hedge_ratio * df["NQ=F"].iloc[i]
        hedge_ratios.append(hedge_ratio)
        spreads.append(spread)
    df["Hedge_Ratio"] = hedge_ratios
    df["Spread"] = spreads
    df.to_csv(output_path, index=False)
    print(f"Spread saved to {output_path}")
    print(f"Rolling window: {window} days")
    score, pvalue, _ = coint(df["ES=F"], df["NQ=F"])
    print(f"Cointegration test p-value: {pvalue:.4f}")

    return df

if __name__ == "__main__":
    calculate_spread()