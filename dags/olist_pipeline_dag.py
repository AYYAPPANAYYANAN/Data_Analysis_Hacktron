# dags/olist_pipeline_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator  # type: ignore[import-not-found]
from datetime import datetime, timedelta
import sys
import os

# Add project root to path for internal module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingestion import load_and_audit_data
from src.features import engineer_features
from src.modeling import train_cost_sensitive_model

default_args = {
    "owner": "mlops-engineer",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": ["mlops-alerts@olist.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_ingestion_and_audit(**context):
    print("Executing scheduled nightly data ingestion and survivorship audit...")
    orders_df = load_and_audit_data(n_samples=20000)
    context['ti'].xcom_push(key='raw_shape', value=orders_df.shape)
    # Save intermediate raw checkpoint
    orders_df.to_parquet("data/raw/nightly_orders.parquet")

def run_feature_engineering(**context):
    print("Executing group-scoped expanding window feature store generation...")
    import pandas as pd
    orders_df = pd.read_parquet("data/raw/nightly_orders.parquet")
    engineered_df = engineer_features(orders_df)
    engineered_df.to_parquet("data/processed/engineered_features.parquet")

def run_model_training(**context):
    print("Executing chronological split model training and asymmetric cost optimization...")
    import pandas as pd
    engineered_df = pd.read_parquet("data/processed/engineered_features.parquet")
    
    valid_delivered = engineered_df[
        (engineered_df["order_status"] == "delivered") & (engineered_df["delivery_delay_days"].notnull())
    ].copy()
    q_low = valid_delivered["delivery_delay_days"].quantile(0.01)
    q_high = valid_delivered["delivery_delay_days"].quantile(0.99)
    cleaned_delivered = valid_delivered[
        (valid_delivered["delivery_delay_days"] >= q_low) & (valid_delivered["delivery_delay_days"] <= q_high)
    ].copy()
    
    train_cost_sensitive_model(cleaned_delivered)

with DAG(
    "olist_logistics_mlops_pipeline",
    default_args=default_args,
    description="Automated daily MLOps pipeline for Olist logistics late-delivery prediction",
    schedule="0 2 * * *", # Run daily at 02:00 UTC
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["mlops", "logistics", "olist"],
) as dag:

    t1 = PythonOperator(
        task_id="ingestion_and_audit",
        python_callable=run_ingestion_and_audit,
        provide_context=True,
    )

    t2 = PythonOperator(
        task_id="feature_engineering",
        python_callable=run_feature_engineering,
        provide_context=True,
    )

    t3 = PythonOperator(
        task_id="model_training_and_registry",
        python_callable=run_model_training,
        provide_context=True,
    )

    t1.set_downstream(t2)
    t2.set_downstream(t3)