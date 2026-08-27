import os
import numpy as np
import pandas as pd

OUT = os.path.join("data", "fraud_windows.csv")

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def main(n=6000, seed=42):
    rng = np.random.default_rng(seed)

    txn_count = rng.integers(80, 1800, n)
    avg_amount = rng.lognormal(mean=np.log(1800), sigma=0.75, size=n)
    failed_rate = rng.beta(1.4, 14, n)
    new_device_rate = rng.beta(2, 8, n)
    high_risk_country_rate = rng.beta(1.5, 18, n)
    chargeback_rate = rng.beta(1.2, 30, n)
    fraud_rate_baseline = rng.uniform(0.002, 0.04, n)
    hour = rng.integers(0, 24, n)

    # Latent risk process: multiple signals jointly create a spike.
    z = (
        -5.2
        + 0.0022 * txn_count
        + 2.4 * (avg_amount / 10000)
        + 8.5 * failed_rate
        + 4.5 * new_device_rate
        + 7.0 * high_risk_country_rate
        + 11.0 * chargeback_rate
        + 5.0 * fraud_rate_baseline
        + 0.55 * ((hour <= 5).astype(float))
        + rng.normal(0, 0.8, n)
    )
    probability = sigmoid(z)
    fraud_spike = rng.binomial(1, probability)

    # Make spike windows visibly different while retaining overlap/noise.
    mask = fraud_spike == 1
    failed_rate[mask] = np.clip(failed_rate[mask] + rng.uniform(.04, .22, mask.sum()), 0, .95)
    new_device_rate[mask] = np.clip(new_device_rate[mask] + rng.uniform(.08, .35, mask.sum()), 0, .98)
    high_risk_country_rate[mask] = np.clip(high_risk_country_rate[mask] + rng.uniform(.03, .28, mask.sum()), 0, .95)
    chargeback_rate[mask] = np.clip(chargeback_rate[mask] + rng.uniform(.02, .20, mask.sum()), 0, .9)
    txn_count[mask] += rng.integers(100, 900, mask.sum())

    df = pd.DataFrame({
        "txn_count": txn_count,
        "avg_amount": np.round(avg_amount, 2),
        "failed_rate": np.round(failed_rate, 5),
        "new_device_rate": np.round(new_device_rate, 5),
        "high_risk_country_rate": np.round(high_risk_country_rate, 5),
        "chargeback_rate": np.round(chargeback_rate, 5),
        "fraud_rate_baseline": np.round(fraud_rate_baseline, 5),
        "hour": hour,
        "fraud_spike": fraud_spike
    })

    os.makedirs("data", exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Created {OUT}")
    print(f"Rows: {len(df)}")
    print(f"Fraud-spike prevalence: {df.fraud_spike.mean():.2%}")

if __name__ == "__main__":
    main()
