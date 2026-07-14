# Dual-Track Portfolio Project: scRNA-seq ML Benchmarking & MLOps

## Project Overview
This repository serves a dual purpose. It demonstrates domain expertise in computational biology (processing high-dimensional single-cell transcriptomic data) AND production-grade Machine Learning Engineering (model lifecycle, experiment tracking, and deployment). By analyzing the public Zheng 68K PBMC dataset, this project proves you can not only build models that understand biology, but also engineer the infrastructure to deploy them.

## Objective
To build a reproducible, end-to-end Machine Learning pipeline that ingests raw single-cell RNA-seq data, preprocesses it, tracks model training experiments across multiple algorithms (e.g., Random Forest vs. PyTorch Deep Neural Network), and deploys the best-performing model as a REST API.

## The Dual-Track Tech Stack
- **Bioinformatics Stack:** Scanpy (preprocessing/QC), AnnData (sparse matrix handling), Snakemake (DAG workflow orchestration).
- **MLOps / ML Engineering Stack:** PyTorch (Deep Learning), MLflow or Weights & Biases (Experiment Tracking), FastAPI (Model Serving), Docker (Containerization), GitHub Actions (CI/CD).

## Repository Structure (Enterprise Standard)
```text
├── .github/workflows/
│   └── ci.yml                 # Automated testing via GitHub Actions
├── data/
│   ├── raw/                   # Immutable downloaded data (Zheng 68k)
│   └── processed/             # QC'd and normalized count matrices
├── notebooks/                 # EDA and biological interpretation
├── src/
│   ├── data_prep.py           # Scanpy QC, normalization, HVG selection
│   ├── models.py              # PyTorch model definitions & Sklearn baselines
│   ├── train.py               # Training loop with MLflow/W&B logging
│   └── evaluate.py            # F1-score, Precision/Recall, Confusion Matrix
├── api/
│   ├── main.py                # FastAPI app to serve the trained model
│   └── Dockerfile             # Container definition for the inference API
├── tests/                     # Pytest suite for data transforms and API endpoints
├── Snakefile                  # Snakemake orchestration (download -> prep -> train)
├── environment.yml            # Conda environment definition
└── README.md                  # Project overview and setup instructions
```

## How to Pitch This Project

### 1. Pitching for Computational Biology Roles
* **The Hook:** "An automated, reproducible pipeline for single-cell RNA-seq cell-type annotation."
* **What to Emphasize:** Highlight your use of **Scanpy** for quality control and normalization. Discuss how you handled biological noise, selected Highly Variable Genes (HVGs), and evaluated the model's performance on rare cell types using macro F1-scores. Emphasize that the workflow is orchestrated with **Snakemake**, making it fully reproducible for large-scale omics datasets.

### 2. Pitching for Machine Learning Engineer Roles
* **The Hook:** "An end-to-end MLOps pipeline for classifying high-dimensional, sparse data (20,000+ features)."
* **What to Emphasize:** The data's origin (biology) is secondary here. Focus on the engineering. Highlight that you built a **PyTorch** classifier for sparse matrices, tracked hyperparameters and model artifacts using **MLflow/W&B**, and packaged the final model into a **Dockerized FastAPI** endpoint for real-time inference. Emphasize your use of **CI/CD** and **pytest** to ensure pipeline reliability.