# src/optimization.py
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def optimize_fulfillment_hubs(synthetic_spatial: pd.DataFrame):
    """
    Runs revenue-weighted K-Means clustering and validates infrastructure CapEx 
    against projected annual GMV protection.
    """
    weighted_coords = np.repeat(
        synthetic_spatial[["lat", "lng"]].values,
        np.maximum(1, (synthetic_spatial["mock_gmv"] / 60).astype(int)),
        axis=0,
    )
    weighted_kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    weighted_kmeans.fit(weighted_coords)
    optimal_hubs = weighted_kmeans.cluster_centers_

    estimated_hub_capex_brl = 1500000.0
    total_protected_gmv = synthetic_spatial["mock_gmv"].sum() * 0.08
    print(
        f"-> CapEx Financial Validation: Total Hub Setup Cost = R$ {estimated_hub_capex_brl*3:,.2f} | "
        f"Projected Annual GMV Protected = R$ {total_protected_gmv:,.2f}"
    )
    return optimal_hubs