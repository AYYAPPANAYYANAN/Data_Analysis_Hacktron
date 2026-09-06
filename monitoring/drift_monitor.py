# monitoring/drift_monitor.py
import pandas as pd
import numpy as np

def detect_feature_drift(reference_df: pd.DataFrame, production_df: pd.DataFrame, feature_name: str) -> float:
    """
    Computes a simplified statistical drift metric (e.g., mean divergence ratio) 
    between historical reference training data and live production incoming data streams.
    """
    ref_mean = reference_df[feature_name].mean()
    prod_mean = production_df[feature_name].mean()
    
    drift_ratio = abs(prod_mean - ref_mean) / (ref_mean + 1e-6)
    
    if drift_ratio > 0.25:
        print(f"[!ALERT!] Significant feature drift detected for '{feature_name}': Drift Ratio = {drift_ratio:.2f}")
    else:
        print(f"-> Feature '{feature_name}' stable. Drift Ratio = {drift_ratio:.2f}")
        
    return drift_ratio