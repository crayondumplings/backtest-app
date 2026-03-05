import streamlit as st
import plotly.graph_objects as go
from backtest import run

st.set_page_config(page_title="Backtest App", layout="wide")
st.title("📈 Stock Backtest Dashboard")

from data import fetch_macro
from strategies import market_regime

# Macro Panel
macro_df = fetch_macro()
regime = market_regime(macro_df)

regime_color = "🟢" if regime['regime'] == "Risk-On" else "🔴"
st.subheader(f"{regime_color} Market Regime: {regime['regime']}")

c1, c2, c3 = st.columns(3)
c1.metric("VIX", f"{regime['vix']:.1f}", delta="< 25 ✓" if regime['vix_ok'] else "> 25 ✗")
c2.metric("Yield Curve", f"{regime['yield_curve']:.2f}", delta="Normal ✓" if regime['yield_curve_ok'] else "Inverted ✗")
c3.metric("Fed Liquidity", f"{regime['fed_balance_sheet']:,.0f}", delta="Expanding ✓" if regime['liquidity_expanding'] else "Contracting ✗")

# Sidebar
ticker = st.sidebar.text_input("Ticker", value="AAPL").upper()
period = st.sidebar.selectbox("Period", ["1y", "2y", "5y", "10y"], index=2)
run_btn = st.sidebar.button("Run Backtest")

if run_btn:
    with st.spinner("Fetching data and running backtest..."):
        df, results = run(ticker, period)

    # Equity curve
    fig = go.Figure()
    colors = {'MA Strategy': 'orange', 'Buy & Hold': 'white', 'DCA': 'green'}
    for name, data in results.items():
        fig.add_trace(go.Scatter(x=data['series'].index, y=data['series'], name=name, line=dict(color=colors[name])))
    fig.update_layout(title=f"{ticker} — Strategy Comparison", template='plotly_dark',
                      xaxis_title='Date', yaxis_title='Portfolio Value (USD)', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # Metrics table
    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    for col, (name, data) in zip([col1, col2, col3], results.items()):
        col.metric(name, f"${data['final']:,.0f}")
        col.write(f"Sharpe: {data['sharpe']:.2f}")
        col.write(f"Max Drawdown: {data['max_drawdown']:.1%}")

    # Winner
    winner = max(results, key=lambda x: results[x]['sharpe'])
    st.success(f"✅ Best risk-adjusted strategy: **{winner}** (Sharpe: {results[winner]['sharpe']:.2f})")