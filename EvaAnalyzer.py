# +
import numpy as np
import matplotlib.pyplot as plt
import pyextremes as pyx
from pyextremes import eva

class EvaAnalyzer:

    def __init__(self, symbol, name, prices):
        self.symbol = symbol
        self.name = name
        self.prices = prices

    def analyze(self):
        self.returns = self.compute_returns()
        self.show_returns()
        self.eva = self.make_eva()
        self.extremes = self.extract_extremes()
        self.show_extremes()
        self.fit_model()
        self.show_model()
        self.get_summary()
        self.show_summary()
        self.make_diagnostic_plots()

    def compute_returns(self):
        returns = np.log(self.prices).diff()
        returns = returns.dropna()
        returns.name = self.symbol
        return returns

    def show_returns(self):
        print(f'\nReturns for {self.symbol}')
        print(self.returns.head())
        print(self.returns.describe())
        plt.figure()
        self.returns.plot(kind='density')

    def make_eva(self):
        myeva = eva.EVA(self.returns)
        return myeva

    def extract_extremes(self):
        self.eva.get_extremes('BM', 'low', block_size='90D')
        return self.eva.extremes

    def show_extremes(self):
        print(f'\nExtremes for {self.symbol}')
        print(self.extremes.head())
        print(self.extremes.describe())
        plt.figure()
        self.extremes.plot(kind='density')
        self.eva.plot_extremes()

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

    def make_diagnostic_plots(self):
        self.eva.plot_diagnostic(alpha=0.95)
