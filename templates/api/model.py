import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import sys
import base64
import os
import pickle
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import timedelta, datetime
import sklearn
from sklearn.preprocessing import MinMaxScaler

from .errors import ValidationError

ML_MODELS = ['ridge', 'lasso', 'gboost', 'nn_1d_lstm']

class Model(object):
    def __init__(self, model_type='ridge'):
        self.type = model_type
        self.model_file = self._load_model()
    
    def __str__(self):
        return self.type
    
    def _load_model(self):
        """
        todo: change this to operate with a db
        """
        filename = self.type + '.sav'
        filepath = os.path.join(os.getcwd(), 'templates/api/models/' + filename)
        exists = os.path.isfile(filepath)
        if not exists:
            raise ValidationError(f"no model file found: {filepath}")
        try:
            model = pickle.load(open(filepath, 'rb'))
        except:
            raise ValidationError('Pickle load unsuccesful')
        return model
    
    def get_model_type(self):
        return self.type
    
    def get_file(self):
        return self.model_file

    def predict_prices(self, data_seed, num_days=10):
        is_nn = self.type == 'nn_1d_lstm'
        if is_nn:
            scaler = MinMaxScaler(feature_range=(-1,1))
            data_seed_norm = scaler.transform(data_seed) # normalized data
            data_seed = data_seed_norm.copy()

        input_values = data_seed
        values = []
        #raise ValidationError(f"model_file: {self.model_file} of type: {type(self.model_file)}")
        for i in range(num_days):
            values.append(self.model_file.predict(input_values)[0])
            # dump the oldest price and put the newest price at the end
            val = input_values
            val = np.insert(val, -1, values[-1], axis=1)
            val = np.delete(val, 0, axis=1)
            input_values = val.copy()
        
        # convert all to numpy arrays
        values = np.array(values)

        # unnormalize prices from Nueral Network approach
        if is_nn:
            values = scaler.inverse_transform(values)[0]
        return values