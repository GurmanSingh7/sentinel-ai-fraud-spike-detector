import os, json, subprocess, sys
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
MODEL_PATH = os.path.join("models", "model.joblib")
METRICS_PATH = os.path.join("models", "metrics.json")

FEATURE_LABELS = {
    "txn_count": "Transaction volume",
    "avg_amount": "Average transaction amount",
    "failed_rate": "Failed-payment rate",
    "new_device_rate": "New-device rate",
    "high_risk_country_rate": "High-risk geography rate",
    "chargeback_rate": "Chargeback rate",
    "fraud_rate_baseline": "Historical fraud baseline",
    "hour": "Unusual transaction hour"
}

def ensure_model():
    if not os.path.exists(os.path.join("data", "fraud_windows.csv")):
        subprocess.check_call([sys.executable, "generate_data.py"])
    if not os.path.exists(MODEL_PATH):
        subprocess.check_call([sys.executable, "train_model.py"])

ensure_model()
bundle = joblib.load(MODEL_PATH)
model, FEATURES = bundle["model"], bundle["features"]

def get_metrics():
    with open(METRICS_PATH) as f:
        return json.load(f)

def explanations(values):
    # Transparent signal explanation independent of model internals.
    signals = []
    checks = [
        ("txn_count", 1000, "Transaction volume is significantly elevated"),
        ("avg_amount", 8000, "Average transaction value is unusually high"),
        ("failed_rate", 0.12, "Failed-payment rate is elevated"),
        ("new_device_rate", 0.45, "Large share of activity comes from new devices"),
        ("high_risk_country_rate", 0.18, "Elevated high-risk geography exposure"),
        ("chargeback_rate", 0.08, "Chargeback signal is elevated"),
        ("fraud_rate_baseline", 0.025, "Merchant has a higher historical fraud baseline"),
    ]
    for key, threshold, text in checks:
        if values[key] >= threshold:
            impact = min(100, round(100 * values[key] / threshold))
            signals.append({"reason": text, "impact": impact})
    if values["hour"] <= 5:
        signals.append({"reason": "Activity occurs during an unusual hour", "impact": 55})
    return sorted(signals, key=lambda x: x["impact"], reverse=True)[:5]

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "model": "loaded"})

@app.get("/api/metrics")
def metrics():
    return jsonify(get_metrics())

@app.post("/api/analyze")
def analyze():
    raw = request.get_json(force=True)
    values = {}
    for feature in FEATURES:
        values[feature] = float(raw.get(feature, 0))
    values["hour"] = int(values["hour"])

    frame = pd.DataFrame([[values[f] for f in FEATURES]], columns=FEATURES)
    probability = float(model.predict_proba(frame)[0, 1])
    risk = round(probability * 100, 1)

    if probability >= 0.75:
        decision = "BLOCK"
        action = "Temporarily restrict the highest-risk payment flow and require step-up verification."
    elif probability >= 0.50:
        decision = "REVIEW"
        action = "Route the spike to merchant risk review and apply step-up verification."
    else:
        decision = "MONITOR"
        action = "Continue monitoring. No immediate restrictive action is recommended."

    window_gmv = values["txn_count"] * values["avg_amount"]
    return jsonify({
        "risk_score": risk,
        "fraud_probability": round(probability, 4),
        "decision": decision,
        "recommended_action": action,
        "signals": explanations(values),
        "window_gmv": round(window_gmv, 2),
        "metrics": get_metrics()
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
