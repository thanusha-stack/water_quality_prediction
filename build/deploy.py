from flask import Flask, request, render_template
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the trained model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))  # Load the scaler used during training

@app.route('/')
def home():
    return render_template('index.html', prediction_text="")  # Reset output on reload

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from form
        ph = float(request.form['ph'])
        hardness = float(request.form['hardness'])
        solids = float(request.form['solids'])
        chloramines = float(request.form['chloramines'])
        sulfate = float(request.form['sulfate'])
        conductivity = float(request.form['conductivity'])
        organic_carbon = float(request.form['organic_carbon'])
        trihalomethanes = float(request.form['trihalomethanes'])
        turbidity = float(request.form['turbidity'])

        # Convert input to array and scale it
        input_data = np.array([[ph, hardness, solids, chloramines, sulfate, conductivity,
                                organic_carbon, trihalomethanes, turbidity]])
        scaled_input = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(scaled_input)

        # Display result
        result = "✅ Water Is Safe To Drink"
        link = None

        if prediction[0] == 0:
            result = "❌ Water Is Not Safe To Drink<br/>"
            link = "https://www.who.int/news-room/fact-sheets/detail/drinking-water"

        return render_template('index.html', prediction_text=result, more_info_link=link)

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
