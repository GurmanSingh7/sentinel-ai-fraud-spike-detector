# Sentinel AI — Fraud Spike Detector

A defensive AI Risk Manager project for detecting abnormal fraud spikes that can lead to merchant losses, chargebacks and unnecessary payment blocks.

## What this project demonstrates

- Binary ML classification: normal vs fraud-spike window
- Reproducible synthetic dataset generation
- Strict train/test split: 80% training, 20% held-out testing
- Precision, Recall and F1-score measured on the held-out test set
- Confusion matrix
- False-positive count and estimated false-positive merchant cost
- Explainable feature contributions
- Interactive Flask dashboard and live scenario simulation

## Project structure

```text
Sentinel_AI_Fraud_Spike_Detector/
│
├── app.py
├── generate_data.py
├── train_model.py
├── requirements.txt
├── README.md
├── data/
├── models/
├── static/
│   ├── app.js
│   └── style.css
└── templates/
    └── index.html
```

# QUICK START — WINDOWS

## 1. Install Python

Install Python 3.10, 3.11 or 3.12.

During installation, tick:

`Add Python to PATH`

Check:

```powershell
python --version
```

## 2. Open PowerShell in the project folder

Extract the ZIP.

Then open PowerShell inside:

```text
Sentinel_AI_Fraud_Spike_Detector
```

## 3. Create a virtual environment

```powershell
python -m venv .venv
```

## 4. Activate it

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## 5. Install dependencies

```powershell
pip install -r requirements.txt
```

## 6. Generate the dataset

```powershell
python generate_data.py
```

## 7. Train and evaluate the ML model

```powershell
python train_model.py
```

This prints Precision, Recall, F1, confusion matrix and false-positive cost.
The test data is held out and is never used for model fitting.

## 8. Run the web application

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

# One-command run after installation

If `data/fraud_windows.csv` and `models/model.joblib` are missing, the Flask app automatically generates data and trains the model.

```powershell
python app.py
```

# API

## Health

`GET /api/health`

## Model metrics

`GET /api/metrics`

## Analyze a risk window

`POST /api/analyze`

Example:

```json
{
  "txn_count": 900,
  "avg_amount": 7200,
  "failed_rate": 0.18,
  "new_device_rate": 0.62,
  "high_risk_country_rate": 0.31,
  "chargeback_rate": 0.12,
  "fraud_rate_baseline": 0.012,
  "hour": 3
}
```

# Buildathon explanation

## Problem

Fraud is not always visible in a single transaction. A merchant can experience a sudden change in payment behaviour: transaction volume jumps, new devices appear, failures increase, high-risk geography increases and chargeback rate rises.

## Solution

Sentinel AI analyzes a short merchant time window and predicts whether the pattern represents a fraud spike.

## Why precision matters

Low precision means too many legitimate merchant periods are flagged, causing unnecessary interventions.

## Why recall matters

Low recall means dangerous fraud spikes are missed.

## False-positive cost

For every false positive, Sentinel estimates an intervention cost:

`txn_count × average_amount × 0.015`

The 1.5% factor is an explicit demo assumption representing estimated lost conversion/operational impact. It is not a claim about real Razorpay costs.

## Important limitation

The included dataset is synthetic and designed for a reproducible demo. In a production system, training data should be based on appropriately governed historical data, temporal validation, monitoring for drift, privacy controls and human review.
