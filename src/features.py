# src/features.py
import pandas as pd

def engineer_features(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies strict chronological sorting and group-scoped shifted expanding windows 
    to prevent target leakage and prediction-time feature latency.
    """
    orders_df["order_year"] = orders_df["order_purchase_timestamp"].dt.year
    orders_df["approval_lag_hours"] = (
        orders_df["order_approved_at"] - orders_df["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600.0
    orders_df["is_peak_macro_season"] = orders_df["order_purchase_timestamp"].dt.month.isin([11, 12]).astype(int)
    
    orders_df["delivery_delay_days"] = (
        orders_df["order_delivered_customer_date"] - orders_df["order_estimated_delivery_date"]
    ).dt.days
    orders_df["is_late"] = (orders_df["delivery_delay_days"] > 0).astype(int)

    # Chronological sort for safe time-series rolling operations
    orders_df = orders_df.sort_values("order_purchase_timestamp").reset_index(drop=True)
    actual_seller_processing = (
        orders_df["order_delivered_carrier_date"] - orders_df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400.0
    orders_df["temp_actual_proc"] = actual_seller_processing

    # Strict Group-Scoped Transform with Shift(1) to eliminate cross-seller leakage
    orders_df["seller_historical_late_rate"] = (
        orders_df.groupby("seller_id")["is_late"]
        .transform(lambda x: x.expanding().mean().shift(1))
        .fillna(0.05)
    )

    orders_df["seller_historical_processing_days"] = (
        orders_df.groupby("seller_id")["temp_actual_proc"]
        .transform(lambda x: x.expanding().mean().shift(1))
        .fillna(3.0)
    )

    return orders_df