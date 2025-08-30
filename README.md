
# ES-NQ-Pairs-Trading

A sector-based pairs trading algorithm and backtesting framework for ES and NQ futures, designed to exploit mean reversion in their price relationship.

## Overview

This project implements a market-neutral statistical arbitrage strategy using the S&P 500 (ES) and Nasdaq 100 (NQ) futures. The workflow includes:

- Fetching and preparing historical futures data
- Performing cointegration and spread analysis with dynamic (rolling) hedge ratios
- Generating trading signals based on z-score thresholds and regime (volatility) filters
- Backtesting the strategy with performance metrics such as Sharpe ratio, drawdown, and hit rate
- Visualizing cumulative returns and trade signals

## Technologies

- Python (Pandas, NumPy, statsmodels, yfinance, matplotlib)

## Project Structure


data/                   # Input and output CSV files
src/
  backtest.py           # Backtesting framework and performance metrics
  data_fetch.py         # Data download and preparation
  spread_calc.py        # Cointegration and rolling spread calculation
  signals.py            # Signal generation with regime filtering
  utils.py              # Plotting utilities
requirements.txt        # Python dependencies


## Usage

1. Fetch historical data:
	
	src/data_fetch.py
	

2. Calculate rolling spread and hedge ratio:
	
	src/spread_calc.py
	

3. Generate trading signals:
	
	src/signals.py
	

4. Run the backtest and visualize results:
	
	src/backtest.py
	

## Notes

- All key parameters (window sizes, thresholds, filters) are easily adjustable in the code for experimentation.
- The framework is designed for flexibility and further research; results will vary depending on parameter choices and market regime.
