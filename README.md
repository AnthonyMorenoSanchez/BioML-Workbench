# BioML Workbench

BioML Workbench is a production-oriented Python package for computational biology and MLOps workflows.
It provides a modular foundation for future omics pipelines, model training, experiment tracking, and deployment.

## Phase 0 Deliverables

- Installable Python package with a clean public API
- YAML-driven configuration and logging infrastructure
- Automated tests and CI workflow
- Docker and Makefile-based developer workflow
- Documentation, changelog, and roadmap updates

## Quick Start

```bash
python -m pip install -e .[dev]
python -m bioml_workbench --show-config
python -m bioml_workbench --run-workflow
```

## End-to-End Workflow

The package now includes a lightweight training workflow that trains a simple classifier, saves metrics and a model artifact, and can be reused as the foundation for larger biological ML pipelines.

```python
from bioml_workbench.workflow import TrainingWorkflow
from bioml_workbench.inference import InferenceService

workflow = TrainingWorkflow(output_dir="artifacts")
result = workflow.run([[0.0, 0.0], [1.0, 1.0]], [0, 1], model_name="simple_logistic")
service = InferenceService("artifacts/model.pkl")
print(service.predict([[0.1, 0.1]]))
```

## API Preview

A minimal FastAPI app is available for serving predictions:

```bash
uvicorn bioml_workbench.api:app --reload
```

## Development Commands

```bash
make test
make lint
make type-check
```

## Configuration

The repository loads `configs/default.yaml` by default and supports environment variable overrides via the `BIOML_` prefix.

For more details, see `docs/configuration.md`.

## Core Utilities

Phase 2 adds reusable utilities for file management, caching, timing, seed control, and configuration lifecycle management.

For more details, see `docs/phase_2.md`.

## Project Layout

- configs/: YAML configuration files
- src/bioml_workbench/: package implementation
- tests/: unit tests
- docs/: project documentation
- pipeline/, ui/, reports/, notebooks/: future extension points
