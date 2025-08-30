import os
import pandas as pd
import numpy as np

def generate_signals(input_path="data/ES_NQ_spread.csv",
                     output_path="data/ES_NQ_signals.csv",
                     window=60,
                     entry_thr=2.0,
                     exit_thr=0.5):
    df = pd.read_csv(input_path, parse_dates=["Date"])
    if "Spread" not in df.columns:
        raise ValueError("Input file must contain a 'Spread' column.")

    df["Spread_Mean"] = df["Spread"].rolling(window=window).mean()
    df["Spread_Std"]  = df["Spread"].rolling(window=window).std()

    df["Z_Score"] = (df["Spread"] - df["Spread_Mean"]) / df["Spread_Std"]

    df["Signal"] = 0
    df.loc[df["Z_Score"] > entry_thr, "Signal"] = -1   # Short ES, Long NQ
    df.loc[df["Z_Score"] < -entry_thr, "Signal"] = 1   # Long ES, Short NQ
    df.loc[df["Z_Score"].abs() < exit_thr, "Signal"] = 0  # Exit positions

    df = df.dropna(subset=["Z_Score"]).reset_index(drop=True)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Signals saved to {output_path} (rows: {len(df)})")
    return df

if __name__ == "__main__":
    generate_signals()