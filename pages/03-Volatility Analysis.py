"""
Volatility Analysis page

- Volatility estimation
- Volatility Regime estimation
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Volatility Analysis')

closing_prices = st.session_state['closing_prices']
sym = st.session_state['sym']
returns = st.session_state['returns']

returns = st.session_state['returns']
window = st.slider('Volatility Window', 2,126,63)

fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(returns)
ax1.set_title(f'{sym} Log-returns')
# Calculate the rolling standard deviation with a 20-day window
rolling_std = returns.rolling(window=window).std()
ax2.plot(rolling_std)
ax2.set_title('Estimated Volatility')
# Define the threshold for high and low volatility
high_threshold_factor = st.slider('High threshold factor', 1.0, 10.0, 1.1, 0.1)
high_vol_threshold = high_threshold_factor * rolling_std.mean()
low_threshold_factor = st.slider('Low threshold factor', 0.1, 1.0, 0.9, 0.01)
low_vol_threshold = low_threshold_factor * rolling_std.mean()

# Create a new DataFrame to store the volatility regime
volatility_regime = pd.DataFrame(index=returns.index, columns=['regime'])

# Classify each period as either high or low volatility
volatility_regime.loc[rolling_std > high_vol_threshold] = 1
volatility_regime.loc[rolling_std < low_vol_threshold] = 0
volatility_regime.fillna(0.5, inplace=True)
ax3.plot(volatility_regime)
ax3.set_xlabel('Year')
ax3.set_ylabel('Regime')
ax3.set_title('Estimated Volatility Regime')
fig.tight_layout()

st.pyplot(fig)