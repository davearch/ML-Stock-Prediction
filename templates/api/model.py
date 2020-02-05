# import packages
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


def plot_prediction(selected_model, values, num_days=10):
    img = io.BytesIO()
    # plot next 10 days
    today = str(datetime.now())
    last_date = datetime.strptime(today[:10], '%Y-%m-%d')
    df_forecast = pd.DataFrame()
    df_forecast[selected_model] = values
    df_forecast.index = pd.date_range(start = last_date, periods=num_days)
    plot = df_forecast.plot(label=selected_model, figsize=(16,8), title='Forecasted Adjusted Closing Price', grid=True)
    fig = plot.get_figure()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)

def get_model(selected_model):
    models = ['ridge_regression', 'lasso', 'gboost', 'nn_1d_lstm']
    if selected_model not in models:
        selected_model = 'ridge_regression'
    filename = selected_model + '.sav'
    filepath = os.path.join(os.getcwd(), 'models/' + filename)
    exists = os.path.isfile(filepath)
    if exists:
        model = pickle.load(open(filepath, 'rb'))
    else:
        print('no model file found', file=sys.stderr)
        return f"error: {filepath} not found"
    return model
    

def load_yahoo_data(stock, start=None):
    """
    download yahoo data from the past 10 days
    """
    if start is None:
        start = datetime.now() - timedelta(days=32)
    yf.pdr_override()
    df = pdr.get_data_yahoo(stock, start=start).reset_index()
    return df

def predict_model(model, data_seed, num_days=10):
    if (model == 'nn_1d_lstm'):
        scaler = MinMaxScaler(feature_range=(-1,1))
        data_seed_norm = scaler.transform(data_seed) # normalized data
        data_seed = data_seed_norm.copy()
    input_values = data_seed
    values = []
    for i in range(num_days):
        values.append(model.predict(data_seed)[0])

        # dump the oldest price and put the newest price at the end
        val = input_values
        val = np.insert(val, -1, values[-1], axis=1)
        val = np.delete(val, 0, axis=1)
        input_values = val.copy()
    
    # convert all to numpy arrays
    values = np.array(values)

    # unnormalize prices from Nueral Network approach
    if (model == 'nn_1d_lstm'):
        values = scaler.inverse_transform(values)[0]

    return values