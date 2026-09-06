# main.py (Updated to include visualization rendering)
from src.ingestion import load_and_audit_data
from src.features import engineer_features
from src.modeling import train_cost_sensitive_model
from src.optimization import optimize_fulfillment_hubs
from src.visualization import render_executive_visualizations
import numpy as np
import pandas as pd

def main():
    print("=" * 70)
    print("OLIST MARKETPLACE: MODULAR ENTERPRISE PIPELINE EXECUTION")
    print("=" * 70)

    # 1. Ingestion
    orders_df = load_and_audit_data(n_samples=15000)

    # 2. Feature Engineering
    orders_df = engineer_features(orders_df)

    valid_delivered = orders_df[
        (orders_df["order_status"] == "delivered") & (orders_df["delivery_delay_days"].notnull())
    ].copy()
    q_low = valid_delivered["delivery_delay_days"].quantile(0.01)
    q_high = valid_delivered["delivery_delay_days"].quantile(0.99)
    cleaned_delivered = valid_delivered[
        (valid_delivered["delivery_delay_days"] >= q_low) & (valid_delivered["delivery_delay_days"] <= q_high)
    ].copy()

    # 3. Modeling
    clf, threshold, feature_importances = train_cost_sensitive_model(cleaned_delivered)

    # 4. Spatial Optimization
    np.random.seed(42)
    synthetic_spatial = pd.DataFrame({
        "lat": np.concatenate([np.random.normal(-23.55, 1.0, 5000), np.random.normal(-8.04, 1.5, 2000)]),
        "lng": np.concatenate([np.random.normal(-46.63, 1.0, 5000), np.random.normal(-34.87, 1.5, 2000)]),
        "mock_gmv": np.concatenate([np.random.exponential(300, 5000), np.random.exponential(500, 2000)]),
    })
    optimal_hubs = optimize_fulfillment_hubs(synthetic_spatial)

    # 5. Executive Visualizations
    render_executive_visualizations(
        orders_df=orders_df,
        cleaned_delivered=cleaned_delivered,
        feature_importances=feature_importances,
        synthetic_spatial=synthetic_spatial,
        optimal_hubs=optimal_hubs
    )

    print("\n" + "=" * 70)
    print("MODULAR REPOSITORY EXECUTION & VISUALIZATION COMPLETED SUCCESSFULLY.")
    print("=" * 70)

if __name__ == "__main__":
    main()