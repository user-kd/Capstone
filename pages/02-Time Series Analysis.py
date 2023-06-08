"""
Time Series analysis page

- Trend-Seasonal-Residual decomposition
- AutoCorrelation Function plot
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf

# Get common data from the first page
closing_prices = st.session_state['closing_prices']
sym = st.session_state['sym']
returns = st.session_state['returns']

st.title('Time Series Analysis')

# Trend-Seasonal-Residual decomposition and plotting
st.subheader(f'Trend-Seasonal Decomposition of {sym} Closing Prices')
fig_seasonal, (ax1,ax2,ax3,ax4) = plt.subplots(4)
ax1.plot(closing_prices[sym])
decomposition = seasonal_decompose(closing_prices[sym], model='additive', period=252)
ax1.set_title(f'{sym} Closing Prices')
ax2.plot(decomposition.trend)
ax2.set_title(f'Extracted trend')
ax3.plot(decomposition.seasonal)
ax3.set_title('Extracted seasonal component')
ax4.plot(decomposition.resid)
ax4.set_title('Residual component')
ax4.set_xlabel('Year')
fig_seasonal.tight_layout()

st.pyplot(fig_seasonal)

# Plot the AutoCorrelation Function
fig_acf, ax_acf = plt.subplots()
plot_acf(returns, ax=ax_acf)
ax_acf.set_title('Autocorrelation plot of log-returns')
st.pyplot(fig_acf)