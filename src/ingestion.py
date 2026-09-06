# src/ingestion.py
import pandas as pd
import numpy as np

def load_and_audit_data(n_samples: int = 15000) -> pd.DataFrame:
    """
    Ingests Olist raw dataset (or robust mock equivalent) and audits order status 
    distribution to prevent survivorship bias.
    """
    dates = pd.date_range(start="2016-01-01", end="2018-10-31", periods=n_samples)
    orders_df = pd.DataFrame({
        "order_id": [f"ord_{i:05d}" for i in range(n_samples)],
        "customer_id": [f"cust_{np.random.randint(1, 5000):05d}" for i in range(n_samples)],
        "seller_id": [f"sell_{np.random.randint(1, 300):05d}" for i in range(n_samples)],
        "order_status": np.random.choice(
            ["delivered", "shipped", "canceled", "unavailable", "processing"],
            size=n_samples,
            p=[0.92, 0.03, 0.02, 0.02, 0.01]
        ),
        "order_purchase_timestamp": dates,
        "order_approved_at": dates + pd.to_timedelta(np.random.exponential(2, n_samples), unit="hours"),
        "order_delivered_carrier_date": dates + pd.to_timedelta(np.random.exponential(3, n_samples), unit="days"),
        "order_delivered_customer_date": dates + pd.to_timedelta(np.random.normal(12, 3, n_samples), unit="days"),
        "order_estimated_delivery_date": dates + pd.to_timedelta(np.random.normal(15, 2, n_samples), unit="days"),
        "mock_gmv": np.random.exponential(200, n_samples) + 50,
        "product_weight_g": np.random.normal(1200, 400, n_samples).clip(100, 10000),
        "freight_to_price_ratio": np.random.beta(2, 8, n_samples),
    })
    
    status_leakage = orders_df["order_status"].value_counts(normalize=True) * 100
    print("-> Order Status Distribution (Survivorship Audit):\n", status_leakage)
    return orders_df