"""
Class for getting closing prices for required symbols
"""

import datetime as dt
import os
import pandas as pd
import yfinance as yf

class ClosingPriceGetter:
    '''
    Get closing price data for required symbols

    1. Find the stocks for which data is not yet downloaded.
    2. Download the required data from the Internet using yfinance
    3. Write the data into CSV files
    3. Read the CSV files for all the required symbols
    5. Extract the closing prices and return in the form of a dict
    '''
    
    def __init__(self, required_syms, data_dir='closing_price_data'):
        self.required_syms = required_syms
        self.data_dir = data_dir
        # Check if data directory exists. If not, create it.
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
    
    def get_closing_prices(self):
        self.get_undownloaded_syms()
        self.download_undowloaded_syms()
        self.read_data_from_csv()
        self.extract_closing_prices_from_csv()
        return self.closing_prices
    
    def is_sym_data_present(self, sym):
        return os.path.exists(f'{self.data_dir}/{sym}.csv')
    
    def get_undownloaded_syms(self):
        self.undownloaded_syms = [
            sym
            for sym in self.required_syms
            if not self.is_sym_data_present(sym)
        ]
    
    def download_undowloaded_syms(self):
        undownloaded_syms = self.undownloaded_syms
        print(f'To download {len(undownloaded_syms)} stocks data.', end='\t')
        print(undownloaded_syms)
        for sym in undownloaded_syms:
            print(f'\tDownloading {sym} data...', end='\t')
            tik = yf.Ticker(sym)
            data = tik.history(period='max')
            data.to_csv(f'{self.data_dir}/{sym}.csv')
            print('DONE')
    
    def read_data_from_csv(self):
        syms = self.required_syms
        data = dict()
        for sym in syms:
            sym_data = pd.read_csv(f'{self.data_dir}/{sym}.csv')
            sym_data['Date'] = pd.to_datetime(
                sym_data['Date'],
                format='%Y-%m-%d'
            )
            sym_data.set_index('Date', inplace=True)
            data[sym] = sym_data
        self.data = data
    
    def extract_closing_prices_from_csv(self):
        closing_prices = dict()
        for key in self.data:
            closing_prices[key] = self.data[key]['Close']
        self.closing_prices = closing_prices