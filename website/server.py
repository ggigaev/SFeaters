import sys
import pickle
from flask import Flask, render_template, request, jsonify, Response
import pandas as pd
import prediction_sf

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '<h1>hello world</h1>'

@app.route('/version', methods=['GET'])
def version():
    return sys.version

@app.route('/inference', methods=['POST'])
def inference():
    req = request.get_json()
    c = req['res_name']
    prediction = prediction_sf.run_predict(c)
    return jsonify({'prediction': prediction})

@app.route('/sfeaters', methods=['GET'])
def SFeaters():
    return render_template('sfeaters.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)
