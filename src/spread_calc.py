import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

def calculate_spread(input_path="data/ES_NQ_daily.csv", output_path="data/ES_NQ_spread.csv"):
    df = pd.read_csv(input_path, parse_dates=["Date"])
    df = df.dropna()
    es = df["ES=F"]
    nq = df["NQ=F"]
    nq_const = sm.add_constant(nq)
    model = sm.OLS(es, nq_const).fit()
    hedge_ratio = model.params["NQ=F"]
    df["Spread"] = model.resid
    df.to_csv(output_path, index=False)
    print(f"Spread saved to {output_path}")
    print(f"Hedge Ratio (beta): {hedge_ratio:.4f}")
    score, pvalue, _ = coint(es, nq)
    print(f"Cointegration test p-value: {pvalue:.4f}")

    return df

if __name__ == "__main__":
    calculate_spread()