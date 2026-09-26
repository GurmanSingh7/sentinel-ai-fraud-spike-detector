import os, json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, accuracy_score

DATA = os.path.join("data", "fraud_windows.csv")
MODEL = os.path.join("models", "model.joblib")

METRICS = os.path.join("models", "metrics.json")

FEATURES = [
    "txn_count", "avg_amount", "failed_rate", "new_device_rate",
    "high_risk_country_rate", "chargeback_rate", "fraud_rate_baseline", "hour"
]

def train():
    df = pd.read_csv(DATA)
    X = df[FEATURES]
    y = df["fraud_spike"]

    # Held-out test set: never passed into fit().
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=350,
        max_depth=12,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # A threshold can be adjusted for business cost. Fixed before reporting test metrics.
    probabilities = model.predict_proba(X_test)[:, 1]
    threshold = 0.50
    predictions = (probabilities >= threshold).astype(int)

    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)
    accuracy = accuracy_score(y_test, predictions)
    tn, fp, fn, tp = confusion_matrix(y_test, predictions, labels=[0,1]).ravel()

    # Demo assumption: intervention on a false alert costs ~1.5% of window GMV.
    test_frame = X_test.copy()
    false_positive_cost = float(
        (test_frame.iloc[(predictions == 1) & (y_test.to_numpy() == 0)]
         ["txn_count"] * test_frame.iloc[(predictions == 1) & (y_test.to_numpy() == 0)]
         ["avg_amount"] * 0.015).sum()
    )

    metrics = {
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1), 4),
        "accuracy": round(float(accuracy), 4),
        "test_samples": int(len(X_test)),
        "train_samples": int(len(X_train)),
        "threshold": threshold,
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        "false_positive_cost": round(false_positive_cost, 2),
        "dataset_note": "Synthetic reproducible demo dataset; held-out test split uses random_state=42."
    }

    os.makedirs("models", exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, MODEL)
    with open(METRICS, "w") as f:
        json.dump(metrics, f, indent=2)

    print("\n=== SENTINEL AI: HELD-OUT TEST RESULTS ===")
    print(f"Train samples: {metrics['train_samples']}")
    print(f"Test samples:  {metrics['test_samples']}")
    print(f"Precision:     {metrics['precision']:.2%}")
    print(f"Recall:        {metrics['recall']:.2%}")
    print(f"F1 Score:      {metrics['f1']:.2%}")
    print(f"Accuracy:      {metrics['accuracy']:.2%}")
    print(f"Confusion Matrix [TN FP / FN TP]: [{tn} {fp}] / [{fn} {tp}]")
    print(f"False-positive cost (demo assumption): ₹{metrics['false_positive_cost']:,.2f}")
    return metrics

if __name__ == "__main__":
    train()
