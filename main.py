'''
Application of statistical techniques for stock selection

This module does the following:
1. Lets the user select a stock for analysis
2. Downloads the closing price data for that stock (if the data is not already present)
3. Displays a plot line plot of the closing prices, and a line plot of log-returns
'''
import streamlit as st
import numpy as np
from ClosingPriceGetter import ClosingPriceGetter
import matplotlib.pyplot as plt

st.title('Pick Stocks')

# Allow the user to select a stock to analyze
syms = ['NVS']
sym = st.selectbox("Stock to analyze", options=syms, index=0)

# Extract closing prices, and save them into common data
closing_prices = ClosingPriceGetter(syms).get_closing_prices()

# Extract and display the date range of the available data
min_date = closing_prices[sym].index.min()
max_date = closing_prices[sym].index.max()
time_span = len(closing_prices[sym])

symbol_summary = f'The data for {sym} is available from:' \
                    f'{min_date:%d %b %Y} to {max_date:%d %b %Y},' \
                    f' for {time_span} trading days.'

st.write(symbol_summary)

# Line plot of closing prices
fig_closing_prices, ax_closing_prices = plt.subplots(figsize=(6,2))
ax_closing_prices.plot(closing_prices[sym])
ax_closing_prices.set_title(f'Closing prices for {sym}')
st.pyplot(fig_closing_prices)

# Extract log-returns and plot them
returns = np.log(closing_prices[sym]).diff().dropna()
fig_returns, ax_returns = plt.subplots(figsize=(6,2))
ax_returns.plot(returns)
ax_returns.set_title(f'Log-returns for {sym}')
st.pyplot(fig_returns)

# Give a toggle option to show/hide the table of closing prices
if st.checkbox('Show closing prices'):
    st.write(closing_prices[sym])

# Save data common to other pages of the application
st.session_state['sym'] = sym
st.session_state['cpg'] = ClosingPriceGetter
st.session_state['dates'] = (min_date, max_date)
st.session_state['closing_prices'] = closing_prices
st.session_state['returns'] = returns