"""
Exploratory data analysis page

- Summary statistics
- Density plot
- Box plot
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Exploratory Data Analysis')

# If the symbol is not set, throw an error
try:
    sym = st.session_state['sym']
    closing_prices = st.session_state['closing_prices']
    returns = st.session_state['returns']
except:
    raise ValueError('No stock selected. Please select the stock from the main page.')

# Two column page layout
text_col, fig_col = st.columns([2,3])

# Extract and write summary statistics
summary_stats = pd.DataFrame(columns=['Closing prices', 'Log-returns'])
summary_stats['Closing prices'] = closing_prices[sym].describe()
summary_stats['Log-returns'] = returns.describe()
text_col.subheader('Summary statistics')
text_col.write(summary_stats)

# Draw the density plot and the box plot
fig_density_boxplot, (ax_density,ax_boxplot) = plt.subplots(2, figsize=(6,6))
returns.plot(ax=ax_density, kind='density')
ax_density.set_title(f'Density plot of {sym} log-returns')
returns.plot(ax=ax_boxplot, kind='box')
ax_boxplot.set_title(f'Box plot of {sym} log-returns')
fig_density_boxplot.tight_layout()
fig_col.subheader(f'Density & Box plots for {sym}')
fig_col.pyplot(fig_density_boxplot)