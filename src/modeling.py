# src/modeling.py (Updated to include model and threshold persistence)
import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_curve

def train_cost_sensitive_model(cleaned_delivered: pd.DataFrame, save_dir: str = "data/processed"):
    """
    Trains a Random Forest classifier using chronological splitting (2016-2017 vs 2018),
    asymmetric cost-matrix threshold tuning, and persists artifacts for API inference.
    """
    os.makedirs(save_dir, exist_ok=True)
    model_features = [
        "approval_lag_hours",
        "seller_historical_processing_days",
        "seller_historical_late_rate",
        "is_peak_macro_season",
        "product_weight_g",
        "freight_to_price_ratio",
    ]
    model_df = cleaned_delivered.dropna(subset=model_features + ["is_late"])

    train_data = model_df[model_df["order_year"].isin([2016, 2017])]
    test_data = model_df[model_df["order_year"] == 2018]

    X_train, y_train = train_data[model_features], train_data["is_late"]
    X_test, y_test = test_data[model_features], test_data["is_late"]

    clf = RandomForestClassifier(
        n_estimators=150, class_weight="balanced_subsample", random_state=42
    )
    clf.fit(X_train, y_train)

    y_proba = clf.predict_proba(X_test)[:, 1]

    # Asymmetric Cost Optimization (False Negatives cost 5x more than False Positives)
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
    costs = []
    for th in thresholds:
        preds = (y_proba >= th).astype(int)
        fn = np.sum((y_test == 1) & (preds == 0))
        fp = np.sum((y_test == 0) & (preds == 1))
        costs.append(5 * fn + 1 * fp)

    optimal_threshold = thresholds[np.argmin(costs)] if len(costs) > 0 else 0.5
    y_pred_optimal = (y_proba >= optimal_threshold).astype(int)

    print(f"-> Optimal Asymmetric Decision Threshold: {optimal_threshold:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred_optimal))
    
    # Persist model artifacts for real-time inference API
    joblib.dump(clf, os.path.join(save_dir, "model.pkl"))
    joblib.dump(optimal_threshold, os.path.join(save_dir, "threshold.pkl"))
    joblib.dump(model_features, os.path.join(save_dir, "features.pkl"))
    print(f"-> Model artifacts successfully saved to '{save_dir}/'")
    
    return clf, optimal_threshold, pd.Series(clf.feature_importances_, index=model_features)