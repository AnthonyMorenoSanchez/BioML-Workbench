# AGENT_INSTRUCTIONS.md

# BioML Workbench
## AI Developer Specification

## Python environment policy
- Always use the workspace virtual environment for Python commands, tests, and package installation.
- Activate the virtual environment before running any Python-related command.
- Install dependencies into the virtual environment only; do not install packages globally.
- If the virtual environment is missing, create it and install required dependencies inside it.
- On Windows, use `.venv\Scripts\python.exe` and `.venv\Scripts\Activate.ps1` for execution.
- Run tests and tooling from the activated environment rather than the system interpreter.

---

# Purpose

You are acting as the lead software engineer for this repository.

Your objective is **NOT** to build isolated scripts.

Your objective is to build a professional, modular, extensible software platform demonstrating modern software engineering, computational biology, machine learning engineering, and MLOps practices.

The finished repository should resemble a mature open-source scientific software package.

Every implementation decision should prioritize

- maintainability
- readability
- extensibility
- reproducibility
- documentation
- testing
- automation

over quickly producing results.

---

# Repository Vision

BioML Workbench is intended to become a reusable machine learning platform for computational biology.

The first implementation focuses on single-cell RNA sequencing (scRNA-seq), but the software architecture must allow future expansion into

- Spatial transcriptomics
- ATAC-seq
- Proteomics
- Imaging
- Multiomics
- Foundation models
- Large language models
- Graph neural networks

No implementation should assume scRNA-seq is the only supported data type.

---

# Development Philosophy

Every feature should be designed as though another developer will extend it.

Avoid monolithic scripts.

Prefer reusable classes.

Prefer dependency injection.

Prefer configuration files over hard-coded values.

Avoid global state.

Document every public function.

Use meaningful names.

Keep functions short.

Keep classes focused.

Never duplicate functionality.

---

# Development Strategy

Build the repository incrementally.

Every phase should leave the repository in a working state.

Never skip foundational infrastructure.

Each phase must include

- implementation
- documentation
- testing
- examples

before progressing.

---

# Repository Architecture

The repository should contain the following top-level modules.

data/

src/

configs/

pipeline/

tests/

ui/

reports/

docs/

.github/

notebooks/

---

# Phase 0
Repository Infrastructure

Goals

Create

- package structure
- pyproject.toml
- requirements
- Docker
- Makefile
- GitHub Actions
- logging
- configuration system
- testing framework

Repository must install successfully.

Repository must pass CI.

---

# Phase 1
Data Engineering

Develop

downloaders

dataset registry

cache manager

validators

data loaders

Supported initially

PBMC68k

Future datasets should only require registering metadata.

No pipeline code should require modification.

---

# Phase 2
Exploratory Data Analysis

Create reusable visualization module.

Avoid notebook-specific plotting.

Visualizations should be callable from

Python

CLI

Dashboard

Generate

QC reports

cell distributions

gene distributions

summary statistics

---

# Phase 3
Preprocessing

Implement

quality control

filtering

normalization

log transformation

feature selection

PCA

neighbors

UMAP

Every preprocessing operation should be configurable through YAML.

---

# Phase 4
Machine Learning

Implement baseline models

Logistic Regression

Random Forest

XGBoost

MLP

Model wrappers should inherit from a common interface.

Future models should require minimal additional code.

---

# Phase 5
Experiment Tracking

Implement

MLflow

Weights & Biases

automatic artifact logging

parameter logging

metric logging

figure logging

model registry

---

# Phase 6
Benchmark Framework

Benchmark

accuracy

macro F1

weighted F1

precision

recall

ROC

PR curves

runtime

memory

training time

inference time

cross validation

confidence intervals

Output

CSV

Markdown

HTML

interactive dashboard

---

# Phase 7
Deployment

Develop

FastAPI

Docker

Swagger

health checks

batch inference

single inference

model versioning

---

# Phase 8
Interactive Dashboard

Framework

Streamlit

The dashboard should feel like a lightweight desktop application.

Pages

Home

Dataset Explorer

QC

Preprocessing

Training

Experiment Browser

Model Comparison

Benchmark Dashboard

Deployment

Settings

Each page should be independent.

Avoid giant Streamlit files.

---

# Phase 9
Continuous Benchmarking

Every completed experiment should automatically

save metrics

save figures

save trained model

generate report

update dashboard

---

# Coding Standards

Python >=3.12

PEP8

Black

Ruff

Pytest

Type hints

Google docstrings

Logging

Pathlib

Dataclasses

Avoid wildcard imports.

Avoid print statements.

Use logging.

---

# Testing

Every module should include tests.

Unit tests

Integration tests

Pipeline tests

Smoke tests

Mock tests

Target

>90% coverage

---

# Documentation

Every module should contain

module documentation

API documentation

examples

usage

developer notes

The docs directory should eventually support MkDocs.

---

# Configuration

Everything configurable.

Never hard-code

paths

hyperparameters

datasets

logging

output folders

Use YAML.

---

# Logging

Implement structured logging.

Support

console

file

future MLflow integration

---

# CLI

Every pipeline component should be executable.

Examples

download

preprocess

train

evaluate

benchmark

dashboard

deploy

Users should never need to modify source code.

---

# Dashboard Requirements

Implement a modern scientific dashboard.

Capabilities

interactive plots

parameter selection

pipeline execution

benchmark comparison

experiment tracking

feature importance

model registry

deployment monitoring

report generation

Dashboard should be attractive, responsive, and modular.

---

# Reports

Automatically generate

Markdown

HTML

PDF (future)

PowerPoint (future)

Include

figures

metrics

tables

configuration

runtime

dataset summary

model summary

---

# Future Features

Architecture should support

DVC

Ray

Optuna

Hydra

Kubeflow

Kubernetes

AWS

Azure

GCP

distributed training

foundation models

multiomics

GPU acceleration

---

# Software Quality

The repository should resemble a production software project.

Every feature should satisfy

documentation

tests

examples

configuration

logging

error handling

before it is considered complete.

---

# Definition of Done

A feature is only complete when

✓ documented

✓ tested

✓ configurable

✓ logged

✓ benchmarked

✓ integrated into dashboard

✓ integrated into CLI

✓ added to documentation

✓ added to changelog

---

# Guiding Principle

Do not build analyses.

Build software.

The repository should eventually become a reusable computational biology machine learning platform demonstrating professional software engineering, reproducible science, modern MLOps, and interactive visualization suitable for industry machine learning engineering and computational biology roles.