from flask import render_template, Blueprint, request, jsonify
import json
from .model import plot_prediction, get_model, load_yahoo_data, predict_model

api_blueprint = Blueprint('api',__name__)


def build_data():
    data = []
    for i in range(10):
        temp = {}
        temp['date'] = f"10-{i+1}"
        temp['val']  = i * 2000
        data.append(temp)
    return data

@api_blueprint.route('/api', methods=['POST'])
def predict():
    if not request.json:
        abort(400)
    stock = request.json.get('stock')
    selected_models = request.json.get('models')
    return jsonify({'stock': stock, 'models': selected_models})
    """
    model = m.get_model(selected_model)

    data_seed = m.load_yahoo_data(stock) # load last 32 days of data
    values = m.predict_model(model, data_seed)
    img = m.plot_prediction(selected_model, values)





    data = build_data()
    return jsonify(data)
    """