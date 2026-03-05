def sharpe_ratio(series, risk_free=0.05):
    daily = series.pct_change().dropna()
    excess = daily - (risk_free / 252)
    return (excess.mean() / excess.std()) * (252 ** 0.5)

def max_drawdown(series):
    peak = series.cummax()
    return ((series - peak) / peak).min()