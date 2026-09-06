# src/visualization.py
import matplotlib
# Force a non-interactive backend configuration safe for headless or standard terminal scripts
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def render_executive_visualizations(
    orders_df: pd.DataFrame, 
    cleaned_delivered: pd.DataFrame, 
    feature_importances: pd.Series, 
    synthetic_spatial: pd.DataFrame, 
    optimal_hubs: np.ndarray,
    save_dir: str = "data/processed"
):
    """
    Renders, saves, and closes the complete 4-chart executive visualization suite 
    preventing non-interactive backend warnings and character artifacts.
    """
    os.makedirs(save_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (12, 6)

    print("\n[Stage 4] Rendering & saving complete executive visualization suite (4 core charts)...")

    # --- Chart 1: Order Status Lifecycle Distribution ---
    plt.figure(figsize=(10, 5))
    status_counts = orders_df["order_status"].value_counts().reset_index()
    status_counts.columns = ["order_status", "count"]
    sns.barplot(
        data=status_counts,
        x="count",
        y="order_status",
        palette="viridis",
        hue="order_status",
        legend=False,
    )
    plt.title("Enterprise Audit: Order Status Lifecycle Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Total Orders", fontsize=12)
    plt.ylabel("Order Status", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "order_status_distribution.png"), dpi=300)
    plt.close()

    # --- Chart 2: Delivery Delay Distribution ---
    plt.figure(figsize=(12, 6))
    sns.histplot(
        data=cleaned_delivered,
        x="delivery_delay_days",
        bins=50,
        kde=True,
        color="#2b5c8f",
    )
    plt.axvline(
        0,
        color="red",
        linestyle="--",
        linewidth=2.5,
        label="Promised Delivery Date (0 Days)",
    )
    plt.title("Olist Logistics Performance: Outlier-Adjusted Delivery Delay Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Delivery Delay in Days (+ = Late, - = Early)", fontsize=12)
    plt.ylabel("Order Frequency", fontsize=12)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "delivery_delay_distribution.png"), dpi=300)
    plt.close()

    # --- Chart 3: Model Interpretability Feature Importance ---
    plt.figure(figsize=(10, 5))
    feature_importances.sort_values().plot(kind="barh", color="#2b5c8f")
    plt.title("Model Interpretability: Key Drivers of Risk (Checkout-Safe Features)", fontsize=14, fontweight="bold")
    plt.xlabel("Feature Importance Score", fontsize=12)
    plt.ylabel("Predictive Features", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "feature_importances.png"), dpi=300)
    plt.close()

    # --- Chart 4: Haversine & Revenue-Weighted Spatial Optimization ---
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=synthetic_spatial.sample(min(2000, len(synthetic_spatial)), random_state=42),
        x="lng",
        y="lat",
        size="mock_gmv",
        hue="mock_gmv",
        palette="viridis",
        alpha=0.6,
        sizes=(20, 200),
    )
    plt.scatter(
        optimal_hubs[:, 1],
        optimal_hubs[:, 0],
        color="red",
        marker="X",
        s=250,
        label="CapEx-Constrained Haversine Hubs",
    )
    plt.title("Prescriptive Facility Location: CapEx-Constrained Network Optimization", fontsize=14, fontweight="bold")
    plt.xlabel("Longitude", fontsize=12)
    plt.ylabel("Latitude", fontsize=12)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "spatial_optimization_hubs.png"), dpi=300)
    plt.close()

    print(f"-> All executive charts successfully generated and saved to '{save_dir}/'")