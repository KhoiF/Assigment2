import os
import pickle
from collections import defaultdict
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from neo4j import GraphDatabase
import numpy as np

app = Flask(__name__)

# --- Models ---
MODEL_OPTIONS = {
    'knn': {'label': 'K-Nearest Neighbors', 'filename': 'knn.sav'},
    'logistic_regression': {'label': 'Logistic Regression', 'filename': 'logistic_regression.sav'},
    'linear_svm': {'label': 'SVM Linear Kernel', 'filename': 'linear_svm.sav'},
    'rbf_svm': {'label': 'SVM RBF Kernel', 'filename': 'rbf_svm.sav'}
}

loaded_models = {}
for model_id, config in MODEL_OPTIONS.items():
    try:
        loaded_models[model_id] = pickle.load(open(config['filename'], "rb"))
    except FileNotFoundError:
        print(f"Warning: Model file {config['filename']} not found.")

FEATURE_COLUMNS = ['Glucose', 'BMI', 'Age', 'Pregnancies', 'SkinThickness', 'Insulin']

# --- Neo4j Config ---
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'neo4j')

neo4j_driver = (
    GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    if NEO4J_PASSWORD
    else None
)

KNOWLEDGE_GROUPS = {
    'HAS_DIET_ADVICE': 'Chế độ ăn',
    'HAS_LIFESTYLE_ACTION': 'Lối sống và vận động',
    'HAS_DRUG_INFO': 'Thông tin thuốc',
    'HAS_COMPLICATION': 'Biến chứng cần lưu ý',
}

def get_diabetes_knowledge():
    """Read grouped diabetes knowledge and article sources from Neo4j."""
    if neo4j_driver is None:
        return [], 'Neo4j password has not been configured (NEO4J_PASSWORD).'
    query = """
    MATCH (d:Disease {id: 'diabetes'})-[relation:HAS_DIET_ADVICE|HAS_LIFESTYLE_ACTION|HAS_DRUG_INFO|HAS_COMPLICATION]->(item)
    OPTIONAL MATCH (item)-[:SOURCED_FROM]->(article:Article)
    RETURN type(relation) AS relation_type,
           coalesce(item.title, item.name) AS title,
           item.content AS content,
           item.duration AS duration,
           item.frequency AS frequency,
           collect(DISTINCT {title: article.title, url: article.url}) AS sources
    ORDER BY relation_type, title
    """
    try:
        grouped_items = defaultdict(list)
        with neo4j_driver.session(database=NEO4J_DATABASE) as session:
            for record in session.run(query):
                sources = [s for s in record['sources'] if s.get('title')]
                grouped_items[record['relation_type']].append({
                    'title': record['title'],
                    'content': record['content'],
                    'duration': record['duration'],
                    'frequency': record['frequency'],
                    'sources': sources
                })
        
        result = []
        for rel_type, label in KNOWLEDGE_GROUPS.items():
            if rel_type in grouped_items:
                result.append({'group_label': label, 'items': grouped_items[rel_type]})
        return result, None
    except Exception as e:
        return [], str(e)


@app.route("/", methods=["GET"])
def home():
    if Path("templates/index.html").exists():
        return render_template("index.html", model_options=MODEL_OPTIONS)
    return "Diabetes Prediction API is running (Neo4j integrated)"


@app.route("/diabetes/v1/predict", methods=["POST"])
def predict():
    features = request.json
    if not isinstance(features, dict):
        return jsonify({"error": "Request must be a JSON object"}), 400

    model_id = features.get("model", "knn")
    if model_id not in loaded_models:
        return jsonify({"error": f"Invalid model. Available models: {list(MODEL_OPTIONS.keys())}"}), 400
    
    selected_model = loaded_models[model_id]

    missing_features = [key for key in FEATURE_COLUMNS if key not in features]
    if missing_features:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_features)}"}), 400

    try:
        features_list = [float(features[feature]) for feature in FEATURE_COLUMNS]
    except ValueError:
        return jsonify({"error": "All feature values must be numeric."}), 400

    prediction = selected_model.predict([features_list])
    
    try:
        confidence = selected_model.predict_proba([features_list])
        confidence_val = round(np.amax(confidence[0]) * 100, 2)
    except Exception:
        # For models like linear SVM that might not have predict_proba enabled by default
        confidence_val = None

    has_diabetes = int(prediction[0]) == 1
    
    knowledge, knowledge_error = [], None
    if has_diabetes:
        knowledge, knowledge_error = get_diabetes_knowledge()

    response = {
        "prediction": int(prediction[0]),
        "confidence": str(confidence_val) if confidence_val is not None else None,
        "model_label": MODEL_OPTIONS[model_id]['label'],
        "knowledge": knowledge,
        "knowledge_error": knowledge_error
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
        use_reloader=False,
    )