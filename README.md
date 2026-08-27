# 🛡️ Sentinel AI — Fraud Spike Detector

> An AI-powered payment risk management system that detects abnormal fraud spikes in merchant payment activity and provides actionable recommendations.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black)
![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-green)

---

## 🚀 Overview

**Sentinel AI** is an AI-powered fraud spike detection system designed to help merchants identify unusual changes in payment behaviour before they potentially lead to increased fraud losses and chargebacks.

Unlike systems that focus on a single transaction, Sentinel AI analyzes **merchant-level payment activity over a specific time window**.

The system evaluates multiple risk signals and predicts whether the current activity should be:

- 🟢 **MONITOR** — Activity appears normal
- 🟠 **REVIEW** — Suspicious activity requires additional verification
- 🔴 **BLOCK** — High probability of a fraud spike

---

## 🎯 Problem Statement

Fraud attacks may not always be visible through a single suspicious transaction.

A merchant may normally have stable payment activity. However, during a potential fraud spike:

- Transaction volume may suddenly increase
- Failed payment attempts may rise
- More transactions may come from new devices
- High-risk geography exposure may increase
- Chargeback signals may increase
- Transaction values may become unusual

Detecting these changes manually can be slow and difficult.

**Sentinel AI analyzes these signals together and identifies abnormal patterns that may indicate a potential fraud spike.**

---

## 💡 Solution

Sentinel AI uses a machine-learning model to analyze merchant payment activity during a specific time window.

### Input Signals

The model analyzes:

- 📊 Transaction volume
- 💰 Average transaction amount
- ❌ Failed-payment rate
- 📱 New-device rate
- 🌍 High-risk geography rate
- 🔄 Chargeback rate
- 📈 Historical fraud baseline
- 🕒 Transaction hour

These signals are passed to a trained **Random Forest classifier**, which predicts the probability of a fraud spike.

The system then provides:

```text
Low Risk      → MONITOR
Medium Risk   → REVIEW
High Risk     → BLOCK
```

---

## 🖥️ How It Works

```text
Merchant Payment Activity
            │
            ▼
    Feature Extraction
            │
            ▼
   Machine Learning Model
     Random Forest
            │
            ▼
   Fraud Spike Probability
            │
            ▼
 ┌──────────┼──────────┐
 ▼          ▼          ▼
MONITOR    REVIEW     BLOCK
```

---

## 🧠 Machine Learning Approach

Sentinel AI uses a **Random Forest Classifier** to classify merchant activity as:

```text
0 → Normal Activity
1 → Fraud Spike
```

The project uses a reproducible synthetic dataset containing merchant payment activity patterns.

### Dataset Split

```text
80% → Training Data
20% → Held-Out Test Data
```

The held-out test set is not used while fitting the model, allowing evaluation on unseen data.

---

## 📊 Model Evaluation

The model is evaluated using:

### Precision
Measures how many activities flagged as fraud spikes were actually fraud spikes.

### Recall
Measures how many actual fraud spikes were successfully detected.

### F1 Score
Provides a balance between Precision and Recall.

### Confusion Matrix

```text
                 Predicted
                 Normal  Spike

Actual Normal       TN      FP
Actual Spike        FN      TP
```

### False-Positive Cost

The project also estimates the potential cost of unnecessary fraud alerts.

> Note: The false-positive cost in this prototype uses a demonstration assumption and does not represent actual Razorpay or merchant costs.

---

## ✨ Features

- 🤖 Machine-learning fraud spike detection
- 📊 Held-out test evaluation
- 🎯 Precision, Recall, and F1 Score
- 🔢 Confusion Matrix
- 💰 False-positive cost estimation
- 🔍 Explainable risk signals
- 🟢 MONITOR recommendation
- 🟠 REVIEW recommendation
- 🔴 BLOCK recommendation
- 🎛️ Interactive dashboard
- ⚡ Safe, Review, and Spike demo scenarios
- 🔌 REST API support

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend and Machine Learning |
| Flask | Web Application |
| Pandas | Data Processing |
| NumPy | Numerical Operations |
| Scikit-learn | Machine Learning |
| Random Forest | Fraud Spike Classification |
| HTML/CSS | User Interface |
| JavaScript | Interactive Dashboard |

---

## 📁 Project Structure

```text
Sentinel_AI_Fraud_Spike_Detector/
│
├── app.py
├── generate_data.py
├── train_model.py
├── requirements.txt
├── README.md
│
├── data/
│   └── fraud_windows.csv
│
├── models/
│   ├── model.joblib
│   └── metrics.json
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── app.js
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/sentinel-ai-fraud-spike-detector.git
```

Move into the project directory:

```bash
cd sentinel-ai-fraud-spike-detector
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> Important: Install `scikit-learn`, not `sklearn`.

---

## 4. Generate the Dataset

```bash
python generate_data.py
```

This creates the synthetic merchant payment activity dataset.

---

## 5. Train the Model

```bash
python train_model.py
```

The training script:

1. Loads the dataset
2. Splits the data into training and held-out test sets
3. Trains the Random Forest model
4. Evaluates Precision, Recall, F1-score, and Accuracy
5. Generates the Confusion Matrix
6. Calculates estimated false-positive cost
7. Saves the trained model

---

## 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

# 🎮 Demo Scenarios

The dashboard includes three predefined scenarios.

## 🟢 Safe

Simulates normal merchant payment activity.

Expected result:

```text
MONITOR
```

---

## 🟠 Review

Simulates suspicious payment activity.

Expected result:

```text
REVIEW
```

---

## 🔴 Spike

Simulates a significant fraud spike with multiple elevated risk signals.

Expected result:

```text
BLOCK
```

---

# 🔌 API

## Analyze Fraud Spike

### Endpoint

```text
POST /api/analyze
```

### Example Request

```json
{
  "txn_count": 1700,
  "avg_amount": 14000,
  "failed_rate": 0.34,
  "new_device_rate": 0.78,
  "high_risk_country_rate": 0.42,
  "chargeback_rate": 0.18,
  "fraud_rate_baseline": 0.035,
  "hour": 3
}
```

### Example Response

```json
{
  "risk_score": 92.4,
  "fraud_probability": 0.924,
  "decision": "BLOCK",
  "recommended_action": "Temporarily restrict the highest-risk payment flow and require step-up verification."
}
```

---

# 📈 Evaluation Methodology

```text
Dataset
   │
   ├── 80% Training Data
   │       │
   │       ▼
   │   Model Training
   │
   └── 20% Held-Out Test Data
           │
           ▼
      Final Evaluation
```

The final model metrics are calculated using the held-out test data.

---

# ⚠️ Limitations

This project is a **prototype created for demonstration and educational purposes**.

The dataset is synthetic and does not contain real customer or merchant payment data.

A production implementation would require:

- Real, properly governed historical data
- Temporal validation
- Feature monitoring
- Model drift detection
- Privacy and security controls
- Human review workflows
- Threshold calibration
- Continuous model evaluation

---

# 🔮 Future Improvements

- Real-time streaming transaction analysis
- Time-series anomaly detection
- Merchant-specific baseline models
- SHAP-based model explainability
- Adaptive risk thresholds
- Alert notifications
- Role-based dashboards
- Human analyst feedback loops
- Model drift monitoring
- Integration with payment APIs

---

# 🎥 Buildathon Demo Flow

For the demo:

1. Open the Sentinel AI dashboard.
2. Explain the fraud-spike problem.
3. Select the **Safe** scenario.
4. Show the **MONITOR** result.
5. Select the **Review** scenario.
6. Show the **REVIEW** result.
7. Select the **Spike** scenario.
8. Show the high-risk result and explanation.
9. Show the model evaluation metrics.
10. Explain Precision, Recall, and F1-score.

---

# 👨‍💻 Author

**Gurman Singh**

Built for an AI Risk Management / Fraud Detection Buildathon.

---

## ⭐ Project Summary

> **Sentinel AI is a machine-learning-powered fraud spike detection system that analyzes merchant payment behaviour, identifies abnormal risk patterns, provides explainable recommendations, and evaluates performance using Precision, Recall, F1-score, and a held-out test set.**
