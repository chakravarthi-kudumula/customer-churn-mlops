## Customer Churn MLops Project ##

# 📊 Customer Retention Analytics & Churn Prediction System

**Production-grade end-to-end ML system for churn prediction with MLOps, CI/CD, and deployment-ready architecture**

---

## 🏷️ Badges

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)  
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)  
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue?logo=mlflow)  
![Docker](https://img.shields.io/badge/Docker-Containerization-blue?logo=docker)  
![CI/CD](https://img.shields.io/badge/GitHub%20Actions-CI/CD-orange?logo=githubactions)  
![XGBoost](https://img.shields.io/badge/XGBoost-Model-red)

---

## 🚀 Project Overview

Customer churn directly impacts revenue and long-term growth. This project builds a **deployable ML system** that not only predicts churn but is structured to reflect **real-world ML engineering workflows**.

**Focus Areas:**
- Reproducibility  
- Maintainability  
- Deployment readiness  
- Industry-standard MLOps practices  

---

## 🧠 Key Highlights

- Modular ML pipeline  
- MLflow-based experiment tracking & model versioning  
- Dockerized application for environment consistency  
- CI/CD integration using GitHub Actions  
- FastAPI-based inference service  
- Clean, scalable project structure aligned with production systems  

---

## 🏗️ Project Structure

    data/
     ├── raw/
     ├── processed/

    src/
     ├── data/               # Data Loading & Validation
     ├── features/           # Feature engineering pipeline
     ├── models/             # Training and inference logic
     ├── utils/              # Shared utilities

    app/
     ├── main.py       # Fast Api entry point
     ├── app.py        # API Logic

    scripts/
     ├── test_pipeline_phase1_data_features.py
     ├── test_pipeline_phase2_modeling.py

    mlruns/                 # MLflow tracking
    artifacts/              # Serialized models
    .github/                # CI?CD workflows

    dockerfile
    requirements.txt

---

## ⚙️ System Workflow (Production-Oriented)

### Data Layer
- Centralized data loading via `src/data/load_data.py`  
- Ensures consistent schema across training & inference  

### Feature Pipeline
- Reusable transformations in `src/features`  
- Guarantees training-serving consistency (same transformations reused)

### Modeling Layer
- Isolated training logic in `src/models`  
- Supports experimentation without breaking pipeline integrity
- Includes threshold tuning to align with business objectives

### Experiment Tracking
- MLflow for:
  - Parameter logging  
  - Metrics tracking  
  - Model versioning  

### Pipeline Validation
- `scripts/` acts as pipeline tests 
- Ensures pipeline reliability 
- Validating :
    - Data ingestion
    - Feature transformations
    - model training flow 

### Inference Layer
- FastAPI service wraps trained model
- Provides real-time prediction endpoint
- Swagger docs for easy testing 

### Containerization
- Docker ensures :
   - Environment reproducibility
   - Smooth deployment across systems

### CI/CD
- GitHub Actions:
  - Code validation on push  
  - Pipeline integrity checks  
  - Deployment readiness  

---

## 🛠️ Tech Stack

**Core:**  
Python, Pandas, NumPy, Scikit-learn, XGBoost  

**MLOps & Backend:**  
MLflow, FastAPI  

**DevOps:**  
Docker, Git, GitHub Actions  

---

## 📦 Installation & Setup

### 1. Clone Repository
    git clone https://github.com/your-username/customer-churn.git
    cd customer-churn

### 2. Create Virtual Environment
    python3 -m venv churn-env
    source churn-env/bin/activate

### 3. Install Dependencies
    pip install -r requirements.txt

---

## ▶️ Running the Pipelines

### Phase 1: Data + Features
    python scripts/test_pipeline_phase1_data_features.py

### Phase 2: Modeling
    python scripts/test_pipeline_phase2_modeling.py

### Whole project pipeline
    python scripts/run_pipeline.py

---

## 🌐 Running the API

    uvicorn app.main:app --reload

- API: http://127.0.0.1:8000  
- Docs: http://127.0.0.1:8000/docs  

---

## 🐳 Docker Usage

### Build Image
    docker build -t churn-app .

### Run Container
    docker run -p 8000:8000 churn-app

---

## 📊 Business Impact & Trade-offs

- Improved identification of high-risk customers using optimized models  
- Enabled proactive retention strategies  
- Designed system for seamless transition from experimentation to production  

### Key Trade-off

**Recall vs Precision Optimization**
- Prioritized higher recall to capture more churn cases  
- **Reason:** Missing a churned customer has higher business cost  
- Accepted increase in false positives to maximize retention  

---

## 🔮 Future Improvements

- MLflow backend migration (DB-based tracking)  
- Model monitoring & drift detection  
- Feature store integration  
- Optimize inference latency for large-scale deployment  

## Support

If you found this project useful:
- Star this repo  
- Fork it  
- Connect on LinkedIn  