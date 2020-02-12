from pandas_datareader import data as pdr
import yfinance as yf
from datetime import timedelta, datetime

from .errors import ValidationError

class Stock(object):
    cache_structure = {} # class-wide cache

    def __init__(self, symbol):
        self.symbol = symbol
        today = datetime.now()
        self.data = self._load_yahoo_data(start=today)

    def __str__(self):
        return self.symbol
    
    def _load_yahoo_data(self, start):
        """
        download yahoo data from the past 32 days
        cache so we don't do a million requests every day
        """
        window_size = 32
        start = start - timedelta(days=32)
        stringdate = start.strftime("%Y-%m-%d")
        #raise ValidationError(f"start is: {start} to string: {stringdate}")
        if stringdate in Stock.cache_structure:
            #raise ValidationError(f"stringdate in cache: {stringdate}")
            return Stock.cache_structure[stringdate]
        yf.pdr_override()
        df = pdr.get_data_yahoo(self.symbol, start=start).reset_index()
        data_seed = df['Adj Close'].values[-window_size:][None]
        Stock.cache_structure[stringdate] = data_seed
        #raise ValidationError(f"data_seed is: {data_seed} of type: {type(data_seed)}")
        return data_seed # returns numpy.ndarray
    
    def get_symbol(self):
        return self.symbol
    
    def get_data(self):
        return self.data