def ma_crossover(df):
    df = df.copy()
    df['MA50'] = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()
    df['Signal'] = 0
    df.loc[(df['MA50'] > df['MA200']) & (df['MA50'].shift(1) < df['MA200'].shift(1)), 'Signal'] = 1
    df.loc[(df['MA50'] < df['MA200']) & (df['MA50'].shift(1) > df['MA200'].shift(1)), 'Signal'] = -1

    cash, shares = 10000, 0
    portfolio = []
    for _, row in df.iterrows():
        if row['Signal'] == 1 and cash > 0:
            shares = cash / row['Close']
            cash = 0
        elif row['Signal'] == -1 and shares > 0:
            cash = shares * row['Close']
            shares = 0
        portfolio.append(cash + shares * row['Close'])
    df['Portfolio'] = portfolio
    return df
    

def buy_and_hold(df):
    df = df.copy()
    df['BuyAndHold'] = 10000 * (df['Close'] / df['Close'].iloc[0])
    return df

def dca(df, monthly=167):
    df = df.copy()
    dca_shares, last_month, values = 0, None, []
    for date, row in df.iterrows():
        if last_month != date.month:
            dca_shares += monthly / row['Close']
            last_month = date.month
        values.append(dca_shares * row['Close'])
    df['DCA'] = values
    return df

def market_regime(macro_df):
    latest = macro_df.iloc[-1]
    
    # Liquidity: is the Fed balance sheet expanding or contracting?
    slope = macro_df['FedBalanceSheet'].diff(30).iloc[-1]
    liquidity_expanding = slope > 0
    
    # Yield curve: inverted = recession warning
    yield_curve_ok = latest['YieldCurve'] > 0
    
    # VIX: high volatility = risk off
    vix_ok = latest['VIX'] < 25
    
    risk_on = liquidity_expanding and yield_curve_ok and vix_ok
    
    return {
        'regime': 'Risk-On' if risk_on else 'Risk-Off',
        'liquidity_expanding': liquidity_expanding,
        'yield_curve_ok': yield_curve_ok,
        'vix_ok': vix_ok,
        'vix': latest['VIX'],
        'yield_curve': latest['YieldCurve'],
        'fed_balance_sheet': latest['FedBalanceSheet']
    }