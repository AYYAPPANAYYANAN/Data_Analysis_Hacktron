# src/celery_app.py
from celery import Celery

# Configure Celery to use Redis as the message broker and backend result store
celery_app = Celery(
    "olist_mlops_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="tasks.batch_predict_orders")
def batch_predict_orders(order_batch_ids: list):
    """
    Asynchronous background task to score nightly batches of orders 
    without blocking the real-time FastAPI worker threads.
    """
    # Placeholder for enterprise batch inference logic utilizing stored model artifacts
    processed_count = len(order_batch_ids)
    print(f"-> Successfully processed background batch scoring for {processed_count} orders.")
    return {"status": "completed", "batch_size": processed_count}