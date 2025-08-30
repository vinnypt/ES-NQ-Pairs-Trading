import os
import pandas as pd
import numpy as np

def generate_signals(input_path="data/ES_NQ_spread.csv",
                     output_path="data/ES_NQ_signals.csv",
                     window=120,
                     entry_thr=1.5,
                     exit_thr=0.3):
    df = pd.read_csv(input_path, parse_dates=["Date"])
    if "Spread" not in df.columns:
        raise ValueError("Input file must contain a 'Spread' column.")


    df["Spread_Mean"] = df["Spread"].rolling(window=window).mean()
    df["Spread_Std"]  = df["Spread"].rolling(window=window).std()
    df["Z_Score"] = (df["Spread"] - df["Spread_Mean"]) / df["Spread_Std"]

    vol_window = 10
    df["Spread_Vol"] = df["Spread"].rolling(window=vol_window).std()
    vol_threshold = df["Spread_Vol"].quantile(0.8)

    df["Signal"] = 0
    low_vol_mask = df["Spread_Vol"] < vol_threshold
    entry_thr_adj = 1.2
    df.loc[low_vol_mask & (df["Z_Score"] > entry_thr_adj), "Signal"] = -1   # Short ES, Long NQ
    df.loc[low_vol_mask & (df["Z_Score"] < -entry_thr_adj), "Signal"] = 1   # Long ES, Short NQ
    df.loc[df["Z_Score"].abs() < exit_thr, "Signal"] = 0  # Exit positions

    df = df.dropna(subset=["Z_Score", "Spread_Vol"]).reset_index(drop=True)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Signals saved to {output_path} (rows: {len(df)})")
    return df

if __name__ == "__main__":
    generate_signals()