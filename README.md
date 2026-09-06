# 🚀 Enterprise-Grade Olist MLOps & Analytics Platform

<p align="center">
  <b>A production-ready, end-to-end MLOps pipeline and advanced analytics platform built for the Olist Brazilian E-commerce dataset (100k+ orders).</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.110+-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Apache_Airflow-Orchestration-017CEE?style=for-the-badge&logo=apache-airflow" alt="Airflow">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/Kubernetes-Clusters-326CE5?style=for-the-badge&logo=kubernetes" alt="Kubernetes">
  <img src="https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions" alt="GitHub Actions">
</p>

---

## 🏗️ Architecture & Tech Stack

| Component | Technology / Framework |
| :--- | :--- |
| **Core Language** | Python 3.13 |
| **API & Real-Time Serving** | FastAPI, Uvicorn |
| **Workflow Orchestration** | Apache Airflow (`olist_pipeline_dag.py`) |
| **Asynchronous Background Tasks** | Celery + Redis |
| **Containerization & Deployment** | Docker, Docker Compose, Kubernetes (`k8s/deployment.yaml`) |
| **CI/CD Automation** | GitHub Actions (`.github/workflows/`) |
| **Testing & Quality Assurance** | Pytest (Strict data leakage verification) |
| **Data Science Stack** | Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn |

---

## 📂 Project Directory Structure

``text

├── .github/

│   └── workflows/
|       |
│       ├── ci.yml                 # Automated testing and leakage verification CI pipeline
|       |
│       └── deploy.yml             # Container build and registry deployment workflow
|       |
├── configs/
|   | 
│   └── model_params.yaml          # Hyperparameters and threshold configurations
|
├── dags/
|   |
│   └── olist_pipeline_dag.py      # Airflow orchestration DAG for batch pipelines
|  
├── data/
|   |
│   ├── processed/                 # Serialized model artifacts, features, and executive charts
|   |
│   └── raw/                       # Olist source CSV datasets
|   |
├── k8s/
|   |
│   └── deployment.yaml            # Production Kubernetes cluster deployment manifests
|
├── monitoring/
|   |
│   └── drift_monitor.py           # Data and concept drift detection system
|
├── src/
|   |
│   ├── __init__.py
|   |
│   ├── celery_app.py              # Asynchronous task worker configurations
|   |
│   ├── features.py                # Leakage-proof feature engineering pipeline
|   |
│   ├── ingestion.py               # Data loading, cleaning, and survivorship audits
|   |
│   ├── modeling.py                # Asymmetric cost-sensitive model training
|   |
│   ├── optimization.py            # CapEx financial optimization and hub placement
|   |
│   └── visualization.py           # Executive chart generation engine
|
├── tests/
|
│   └── test_leakage.py            # Pytest suite for strict data leakage checks
|
├── app.py                         # FastAPI real-time inference server
|
├── main.py                        # End-to-end local MLOps execution pipeline
|
├── run_system.py                  # Single-prompt execution wrapper for the full system
|
├── Dockerfile                     # Production container build instructions
|
├── docker-compose.yml             # Multi-container orchestration setup
| 
└── requirements.txt               # Project dependencies
⚡ Key Features & Engineering Highlights
🔒 Leakage-Proof Feature Engineering (src/features.py): Built with strict temporal separation to prevent target leakage during feature generation, validated automatically via tests/test_leakage.py.

⚖️ Asymmetric Cost-Sensitive Modeling (src/modeling.py): Optimizes decision thresholds dynamically (e.g., threshold set at 0.2867) to heavily penalize False Negatives (missed logistics delays) over False Positives, protecting customer satisfaction.

💰 Financial & CapEx Validation (src/optimization.py): Directly maps model predictions to business metrics, computing hub setup costs against projected annual GMV protection.

🔄 Automated CI/CD Pipelines: Validates code health, runs automated Pytest leakage tests, and pushes container artifacts to registries on every merge to main.

🚀 Quick Start & Local Execution
1. Install Dependencies
Bash
pip install -r requirements.txt
2. Run the Entire System via Single-Prompt Wrapper
Execute the complete end-to-end pipeline and instantly spin up the FastAPI server:

Bash
python run_system.py
3. Execution Console Output Log
Plaintext
=== Step 1: Executing Olist Pipeline Training & Artifact Generation ===
======================================================================
OLIST MARKETPLACE: MODULAR ENTERPRISE PIPELINE EXECUTION
======================================================================
-> Order Status Distribution (Survivorship Audit):
order_status
delivered       92.093333
shipped          2.960000
unavailable      2.073333
canceled         1.793333
processing       1.080000
Name: proportion, dtype: float64
-> Optimal Asymmetric Decision Threshold: 0.2867

Classification Report:
              precision    recall  f1-score   support

           0       0.87      0.98      0.92      3456
           1       0.23      0.03      0.06       544

    accuracy                           0.85      4000
   macro avg       0.55      0.51      0.49      4000
weighted avg       0.78      0.85      0.80      4000

-> Model artifacts successfully saved to 'data/processed/'
-> CapEx Financial Validation: Total Hub Setup Cost = R$ 4,500,000.00 | Projected Annual GMV Protected = R$ 205,954.45

[Stage 4] Rendering & saving complete executive visualization suite (4 core charts)...
-> All executive charts successfully generated and saved to 'data/processed/'

======================================================================
MODULAR REPOSITORY EXECUTION & VISUALIZATION COMPLETED SUCCESSFULLY.
======================================================================

=== Step 2: Launching FastAPI Real-Time Inference Server ===
INFO:     Will watch for changes in these directories: ['C:\\Users\\Ayyappan\\Desktop\\1']
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
INFO:     Started reloader process [3276] using WatchFiles
INFO:     Started server process [14364]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
🌐 Access Live API & Documentation
API Root Endpoint: http://127.0.0.1:8000

Interactive Swagger UI: http://127.0.0.1:8000/docs

🐳 Docker & Container Deployment
To run the complete platform services via Docker Compose:

Bash
docker-compose up --build
