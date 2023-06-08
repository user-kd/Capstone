"""
Extreme value analysis page

- Identification of extreme values (Monthly Minima)
- Plotting the probability density of the Monthly Minima
- Diagnostic plots of the Extreme Value modelling
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pyextremes as pyx
from pyextremes import eva

closing_prices = st.session_state["closing_prices"]
returns = st.session_state['returns']
sym = st.session_state['sym']

st.title('Extreme Value Analysis')


class EvaAnalyzer:
    """
    Class containing functions for conducting an Extreme Value Analysis

    Usage: EvaAnalyzer(sym, returns)
    """
    def __init__(self, symbol, returns):
        self.symbol = symbol
        self.returns = returns

    def analyze(self):
        self.eva = self.make_eva()
        self.extremes = self.extract_extremes()
        self.fit_model()

    def make_eva(self):
        myeva = eva.EVA(self.returns)
        return myeva

    def extract_extremes(self):
        self.eva.get_extremes('BM', 'low', block_size='90D')
        return self.eva.extremes

    def make_extremes_lineplot_fig(self):
        fig, ax = plt.subplots()
        self.eva.plot_extremes(ax=ax)
        ax.set_title(f'Identification of Extreme {sym} log-returns')
        return fig
    
    def make_extremes_density_fig(self):
        fig, ax = plt.subplots()
        self.extremes.plot(kind='density', ax=ax)
        ax.set_title('Estimated density of monthly minimum log-returns')
        ax.set_xlabel('Log-return')
        return fig

    def fit_model(self):
        self.eva.fit_model('MLE')

    def show_model(self):
        print(self.eva)

    def get_summary(self):
        self.summary = self.eva.get_summary(
            return_period=[1, 2, 3, 5, 6, 7, 8, 10, 12, 15, 20],
            alpha=0.95,
            n_samples=1000,
        )

    def show_summary(self):
        print(self.summary)

    def make_diagnostic_fig(self):
        fig, *axs = self.eva.plot_diagnostic(alpha=0.95)
        fig.suptitle('Diagnostic plots for Extreme Value modelling')
        return fig

eva_analyzer = EvaAnalyzer(sym, returns)
eva_analyzer.analyze()

col1, col2 = st.columns(2)

# Create line plot where Monthly Minima are marked
extremes_lineplot_fig = eva_analyzer.make_extremes_lineplot_fig()
col1.pyplot(extremes_lineplot_fig)

# Create the density plot for the Monthly Minima
extremes_density_fig = eva_analyzer.make_extremes_density_fig()
col2.pyplot(extremes_density_fig)

# Create the diagnostic plots for Extreme Value modelling
extremes_diagnostic_fig = eva_analyzer.make_diagnostic_fig()
st.pyplot(extremes_diagnostic_fig)