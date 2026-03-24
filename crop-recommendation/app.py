from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)   


model = joblib.load("crop_model.pkl")
scaler = joblib.load("scaler.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[
        data["nitrogen"],
        data["phosphorous"],
        data["potassium"],
        data["temperature"],
        data["humidity"],
        data["ph"],
        data["rainfall"]
    ]])

    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]

    probabilities = model.predict_proba(features_scaled)[0]
    confidence = float(max(probabilities) * 100)

    top_3_idx = np.argsort(probabilities)[-3:][::-1]

    top_3_crops = [
        {
            "name": model.classes_[i],
            "confidence": float(probabilities[i] * 100)
        }
        for i in top_3_idx
    ]

    return jsonify({
        "success": True,
        "prediction": prediction,
        "confidence": confidence,
        "top_3_crops": top_3_crops
    })


if __name__ == "__main__":
    app.run(debug=True)