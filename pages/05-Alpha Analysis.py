"""
Alpha analysis page

- Give the menu to choose a benchmark
- Download data for the benchmark if required
- Compute the stock's alpha wrt the benchmark
- Show a visualization of the alpha and beta
"""

import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import statsmodels.api as sm

sym_closing_prices = st.session_state["closing_prices"]
sym_returns = st.session_state['returns']
sym = st.session_state['sym']
sym_min_date, sym_max_date = st.session_state['dates']
ClosingPriceGetter = st.session_state['cpg']

st.title('Alpha Analysis')

benchmark_choices = ['S&P 500']
bm_choice = st.selectbox(
    'Benchmark for alpha computation:',
    options=benchmark_choices,
    index=0
)

benchmark_sym_dict = {
    'S&P 500': 'SPY'
}

risk_free_rate_pct_annual = st.slider(
    label = 'Annual risk-free rate',
    min_value = 0.0,
    max_value = 0.2,
    value = 0.03,
    step = 0.01
)
risk_free_rate = np.log(1 + risk_free_rate_pct_annual)/252  # Convert to daily log-return

bm_sym = benchmark_sym_dict[bm_choice]
bm_raw_data = yf.download(bm_sym, start=sym_min_date, end=sym_max_date)
bm_closing_prices = bm_raw_data['Close']
bm_returns = np.log(bm_closing_prices).diff().dropna()

bm_min_date = bm_returns.index.min()
bm_max_date = bm_returns.index.max()
st.write(f'Benchmark data available from: {bm_min_date:%d %b %Y} to {bm_max_date:%d %b %Y}')

min_date = max(bm_min_date, sym_min_date)
max_date = min(bm_max_date, sym_max_date)
st.write(f'Data for both, stock and benchmark, available from {min_date:%d %b %Y} to {max_date:%d %b %Y}')

sym_returns = sym_returns.loc[min_date:max_date]
bm_returns = bm_returns.loc[min_date:max_date][1:]
# The [1:] compensates for a day lost due to diff and dropna


# Beta estimation
bm_excess_returns = bm_returns - risk_free_rate
sym_excess_returns = sym_returns - risk_free_rate
X = sm.add_constant(bm_excess_returns)
y = sym_excess_returns
ols_model = sm.OLS(y, X).fit()
beta = ols_model.params[1]

fig, ax = plt.subplots()
ax.plot(bm_excess_returns, sym_excess_returns, lw=0, marker='o')
ax.set_title(f'Excess returns of benchmark and {sym}')
ax.set_xlabel(f'Excess benchmark ({bm_choice}) returns')
ax.set_ylabel(f'Excess {sym} returns')
st.pyplot(fig)

# Alpha estimation
alpha_values = sym_excess_returns - beta*bm_excess_returns
alpha = alpha_values.mean()
alpha_annualized = alpha * np.sqrt(252)

st.write(f'Beta: {beta:.3}')
st.write(f'Alpha (annualized): {alpha_annualized:.5}')