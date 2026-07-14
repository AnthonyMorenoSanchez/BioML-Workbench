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

## Project Layout

- configs/: YAML configuration files
- src/bioml_workbench/: package implementation
- tests/: unit tests
- docs/: project documentation
- pipeline/, ui/, reports/, notebooks/: future extension points
