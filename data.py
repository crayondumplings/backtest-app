import yfinance as yf
import pandas as pd
from fredapi import Fred
import streamlit as st

FRED_API_KEY = st.secrets["FRED_API_KEY"]

def fetch(ticker, period="5y"):
    data = yf.Ticker(ticker).history(period=period)
    data.index = data.index.tz_localize(None)
    return data

def fetch_macro():
    fred = Fred(api_key=FRED_API_KEY)
    
    # Fed Balance Sheet
    walcl = fred.get_series("WALCL").rename("FedBalanceSheet")
    
    # Yield Curve (10Y - 2Y)
    t10y2y = fred.get_series("T10Y2Y").rename("YieldCurve")
    
    # VIX via yfinance
    vix = yf.Ticker("^VIX").history(period="5y")["Close"].rename("VIX")
    vix.index = vix.index.tz_localize(None)
    
    # Combine into one DataFrame
    macro = pd.concat([walcl, t10y2y, vix], axis=1)
    macro = macro.ffill().dropna()
    return macro