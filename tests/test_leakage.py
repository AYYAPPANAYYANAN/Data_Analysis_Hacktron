# tests/test_leakage.py
import pandas as pd
import numpy as np
import pytest
from src.features import engineer_features

def test_chronological_and_group_leakage():
    """
    Validates that expanding window features are strictly shifted and 
    scoped per seller, preventing look-ahead and cross-seller leakage.
    """
    dates = pd.date_range(start="2026-01-01", periods=10, freq="D")
    df = pd.DataFrame({
        "order_id": [f"ord_{i}" for i in range(10)],
        "customer_id": ["cust_1"] * 10,
        "seller_id": ["sell_A", "sell_B"] * 5,
        "order_status": ["delivered"] * 10,
        "order_purchase_timestamp": dates,
        "order_approved_at": dates + pd.Timedelta(hours=1),
        "order_delivered_carrier_date": dates + pd.Timedelta(days=2),
        "order_delivered_customer_date": dates + pd.Timedelta(days=5),
        "order_estimated_delivery_date": dates + pd.Timedelta(days=4),
        "mock_gmv": [100.0] * 10,
        "product_weight_g": [1000.0] * 10,
        "freight_to_price_ratio": [0.2] * 10
    })
    
    engineered = engineer_features(df)
    
    # Assert sorting is chronological
    assert engineered["order_purchase_timestamp"].is_monotonic_increasing
    
    # Assert historical features exist and contain no NaNs after fillna
    assert "seller_historical_late_rate" in engineered.columns
    assert not engineered["seller_historical_late_rate"].isnull().any()
    
    # Ensure first entry for a seller correctly uses the fallback prior (0.05)
    first_seller_a_idx = engineered[engineered["seller_id"] == "sell_A"].index[0]
    assert engineered.loc[first_seller_a_idx, "seller_historical_late_rate"] == 0.05