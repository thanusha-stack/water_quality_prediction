import os
import logging
import pickle
import numpy as np
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return redirect('/build/home.html')

@app.route('/<path:folder>/<path:filename>')
def serve_static_folders(folder, filename):
    # Allow serving static files natively from the project's frontend directories
    if folder in ['build', 'templates', 'map']:
        return send_from_directory(folder, filename)
    return "Not Found", 404


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

logging.basicConfig(level=logging.DEBUG)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()
        input_values = [
            float(data['ph']),
            float(data['hardness']),
            float(data['solids']),
            float(data['chloramines']),
            float(data['sulfate']),
            float(data['conductivity']),
            float(data['organic_carbon']),
            float(data['trihalomethanes']),
            float(data['turbidity'])
        ]
        logging.debug(f"Raw Input: {input_values}")

        input_data = np.array(input_values).reshape(1, -1)

        # Scale the input data
        input_data_scaled = scaler.transform(input_data)
        logging.debug(f"Scaled Input: {input_data_scaled}")

        prediction = model.predict(input_data_scaled)
        result = int(prediction[0])

        return jsonify({
            'result': result,
            'message': '✅ Water Is Safe To Drink' if result == 1 else '❌ Water Is Not Safe To Drink'
        })

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
