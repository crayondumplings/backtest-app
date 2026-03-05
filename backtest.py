from data import fetch, fetch_macro
from strategies import ma_crossover, buy_and_hold, dca
from metrics import sharpe_ratio, max_drawdown

def run(ticker, period="5y"):
    df = fetch(ticker, period)
    df = ma_crossover(df)
    df = buy_and_hold(df)
    df = dca(df)
    
    results = {}
    for name, col in [
        ('MA Strategy', 'Portfolio'),
        ('Buy & Hold', 'BuyAndHold'),
        ('DCA', 'DCA')
    ]:
        results[name] = {
            'series': df[col],
            'sharpe': sharpe_ratio(df[col]),
            'max_drawdown': max_drawdown(df[col]),
            'final': df[col].iloc[-1]
        }
    
    return df, results