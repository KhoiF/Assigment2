import os
import pickle
from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# --- Load Models & Preprocessor ---
MODEL_OPTIONS = {
    'linear_regression': {'label': 'Linear Regression', 'filename': 'models/linear_regression.sav'},
    'decision_tree': {'label': 'Decision Tree Regressor', 'filename': 'models/decision_tree.sav'},
    'random_forest': {'label': 'Random Forest Regressor', 'filename': 'models/random_forest.sav'},
    'svr': {'label': 'Support Vector Regression (SVR)', 'filename': 'models/svr.sav'}
}

loaded_models = {}
for model_id, config in MODEL_OPTIONS.items():
    try:
        loaded_models[model_id] = pickle.load(open(config['filename'], "rb"))
    except FileNotFoundError:
        print(f"Warning: Model file {config['filename']} not found.")

try:
    preprocessor = pickle.load(open("models/preprocessor.sav", "rb"))
except FileNotFoundError:
    preprocessor = None
    print("Warning: preprocessor.sav not found.")

FEATURE_COLUMNS = ['Floors', 'Bedrooms', 'Bathrooms', 'Legal status', 'Furniture state']

@app.route('/')
def index():
    return render_template('index.html', model_options=MODEL_OPTIONS)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "Request must be a JSON object"}), 400

    model_id = data.get("model", "decision_tree")
    if model_id not in loaded_models:
        return jsonify({"success": False, "error": f"Invalid model. Available: {list(MODEL_OPTIONS.keys())}"}), 400
    
    selected_model = loaded_models[model_id]
    if preprocessor is None:
        return jsonify({"success": False, "error": "Preprocessor not loaded."}), 500

    missing_features = [key for key in FEATURE_COLUMNS if key not in data]
    if missing_features:
        return jsonify({"success": False, "error": f"Missing required fields: {', '.join(missing_features)}"}), 400

    try:
        # Construct DataFrame for the preprocessor
        input_data = pd.DataFrame([{
            'Floors': float(data['Floors']),
            'Bedrooms': float(data['Bedrooms']),
            'Bathrooms': float(data['Bathrooms']),
            'Legal status': str(data['Legal status']),
            'Furniture state': str(data['Furniture state'])
        }])
        
        # Preprocess features
        X_proc = preprocessor.transform(input_data)
        
        # Predict
        prediction = selected_model.predict(X_proc)
        predicted_price = float(prediction[0])
        
        return jsonify({
            'success': True, 
            'price': round(predicted_price, 2),
            'model_label': MODEL_OPTIONS[model_id]['label']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
