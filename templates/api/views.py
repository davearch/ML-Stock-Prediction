from flask import render_template, Blueprint, request, jsonify
import json
from . import api
from .model import Model
from .stock import Stock
#from .model import plot_prediction, get_model, load_yahoo_data, predict_model, load_models

from .errors import ValidationError

def _build_data():
    data = []
    for i in range(10):
        temp = {}
        temp['date'] = f"10-{i+1}"
        temp['val']  = i * 2000
        data.append(temp)
    return data

@api.route('/', methods=['POST'])
def predict():
    selected_stock = request.json.get('stock')
    selected_models = request.json.get('models')

    models = [x for x,y in selected_models.items() if y]
    if not models or not selected_stock:
        raise ValidationError('nothing requested')
    # should change input to radio select tbh
    first = models[0] # just get the first for now

    loaded_model = Model(first)
    stock = Stock(selected_stock)

    prediction = loaded_model.predict_prices(stock.get_data())

    return jsonify({'resp': 'ok', 'data': prediction.tolist()})

    """
    model = m.get_model(selected_model)

    data_seed = m.load_yahoo_data(stock) # load last 32 days of data
    values = m.predict_model(model, data_seed)
    img = m.plot_prediction(selected_model, values)

    data = build_data()
    return jsonify(data)
    """