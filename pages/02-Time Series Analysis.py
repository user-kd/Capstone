"""
Time Series analysis page

- Trend-Seasonal-Residual decomposition
- AutoCorrelation Function plot
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller

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

def compute_rms(seq):
    return np.sqrt(np.mean(seq**2))

rms_cp = compute_rms(closing_prices[sym])
rms_trend = compute_rms(decomposition.trend)
rms_seasonal = compute_rms(decomposition.seasonal)
rms_resid = compute_rms(decomposition.resid)

rms_cp_recent = compute_rms(closing_prices[sym][-1000:])
rms_trend_recent = compute_rms(decomposition.trend[-1000:])
rms_seasonal_recent = compute_rms(decomposition.seasonal[-1000:])
rms_resid_recent = compute_rms(decomposition.resid[-1000:])

st.table(
    pd.DataFrame(
        {
            'RMS of\nentire series': [
                rms_cp,
                rms_trend,
                rms_seasonal,
                rms_resid
            ],
            'RMS of last\n1000 trading days': [
                rms_cp_recent,
                rms_trend_recent,
                rms_seasonal_recent,
                rms_resid_recent
            ],
        },
        index = [
            'Closing Price series',
            'Trend component',
            'Seasonal component',
            'Residual component',
        ]
    )
)

adf_p_value = adfuller(decomposition.resid.dropna())[1]
st.write(f'The p-value of the Augmented Dickey-Fuller test is: {adf_p_value:.3}')  

# Plot the AutoCorrelation Function
fig_acf, ax_acf = plt.subplots()
plot_acf(returns, ax=ax_acf)
ax_acf.set_title('Autocorrelation plot of log-returns')
st.pyplot(fig_acf)
