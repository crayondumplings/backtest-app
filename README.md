# Stock Backtest Dashboard

A quantitative macro-ML backtesting app built with Python and Streamlit.

## Features
- Backtest 3 strategies: MA Crossover, Buy & Hold, DCA
- Macro regime indicator: VIX, Yield Curve, Fed Liquidity (FRED API)
- Interactive Plotly equity curve + performance metrics (Sharpe, Max Drawdown)

## Stack
Python, yfinance, pandas, numpy, streamlit, plotly, fredapi

## Run Locally
pip install -r requirements.txt
streamlit run app.py
