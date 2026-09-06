### Enterprise-Grade Olist MLOps & Analytics Platform
A production-ready, end-to-end MLOps pipeline and advanced analytics platform built for the Olist Brazilian E-commerce dataset (100,000+ orders). This repository bridges exploratory data analysis with enterprise-grade systems architecture, featuring leakage-proof feature stores, cost-sensitive machine learning, real-time FastAPI serving, asynchronous Celery workers, Airflow pipeline orchestration, and automated CI/CD workflows via GitHub Actions.

Architecture & Tech Stack
Core Language: Python 3.13

API & Serving: FastAPI, Uvicorn

Orchestration: Apache Airflow (olist_pipeline_dag.py)

Background Tasks: Celery + Redis

Containerization: Docker, Docker Compose, Kubernetes (k8s/deployment.yaml)

CI/CD Automation: GitHub Actions (.github/workflows/)

Testing & Quality Assurance: Pytest (rigorous data leakage verification)

Data Science & Modeling: Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn

### Project Directory Structure
├── .github/workflows/
│   ├── ci.yml                 # Automated testing and leakage verification CI pipeline
│   └── deploy.yml             # Container build and registry deployment workflow
├── configs/
│   └── model_params.yaml      # Hyperparameters and threshold configurations
├── dags/
│   └── olist_pipeline_dag.py  # Airflow orchestration DAG for batch pipelines
├── data/
│   ├── processed/             # Serialized model artifacts, features, and executive charts
│   └── raw/                   # Olist source CSV datasets
├── k8s/
│   └── deployment.yaml        # Production Kubernetes cluster deployment manifests
├── monitoring/
│   └── drift_monitor.py       # Data and concept drift detection system
├── src/
│   ├── __init__.py
│   ├── celery_app.py          # Asynchronous task worker configurations
│   ├── features.py            # Leakage-proof feature engineering pipeline
│   ├── ingestion.py           # Data loading, cleaning, and survivorship audits
│   ├── modeling.py            # Asymmetric cost-sensitive model training
│   ├── optimization.py        # CapEx financial optimization and hub placement
│   └── visualization.py       # Executive chart generation engine
├── tests/
│   └── test_leakage.py        # Pytest suite for strict data leakage checks
├── app.py                     # FastAPI real-time inference server
├── main.py                    # End-to-end local MLOps execution pipeline
├── run_system.py              # Single-prompt execution wrapper for the full system
├── Dockerfile                 # Production container build instructions
├── docker-compose.yml         # Multi-container orchestration setup
└── requirements.txt           # Project dependencies

### Key Features & Engineering Highlights
Leakage-Proof Feature Engineering (src/features.py): Built with strict temporal separation to prevent target leakage during feature generation, validated automatically via tests/test_leakage.py.

Asymmetric Cost-Sensitive Modeling (src/modeling.py): Optimizes decision thresholds dynamically (e.g., threshold set at 0.2867) to heavily penalize False Negatives (missed logistics delays) over False Positives, protecting customer satisfaction.

Financial & CapEx Validation (src/optimization.py): Directly maps model predictions to business metrics, computing hub setup costs against projected annual GMV protection.

Automated CI/CD Pipelines: Validates code health, runs automated Pytest leakage tests, and pushes container artifacts to registries on every merge to main.

### Quick Start & Local Execution
1. Install Dependencies
   # pip install -r requirements.txt

2. Run the Entire System via Single-Prompt Wrapper
To execute the complete end-to-end pipeline (data ingestion, feature engineering, asymmetric model training, artifact serialization, chart generation) and instantly spin up the FastAPI server, run:
  # python run_system.py

3. Access Live API & Documentation
Once the server is active, navigate to your browser to view the interactive Swagger documentation:

  API Root: http://127.0.0.1:8000

  Swagger UI: http://127.0.0.1:8000/docs

### Docker & Container Deployment
To run the complete platform services via Docker Compose:
 # docker-compose up --build

### Run the output
#  python run_system.py  


