# Roadmap

## Phase 0 — Repository Foundation (Completed)
- Established the package structure and Python packaging metadata.
- Added configuration, logging, CI, Docker, and development tooling.
- Added tests and developer documentation.

## Phase 1 — Configuration System (Completed)
- Expanded YAML-driven configuration to include dataset, training, and dashboard sections.
- Added environment variable overrides and config path resolution.

## Phase 2 — Core Utilities (Completed)
- Added a file manager, cache manager, timer utilities, and seed management.
- Added reusable exception handling and configuration lifecycle management.

## Phase 3 — Data Engineering (Completed)
- Added a dataset registry for known datasets and metadata lookup.
- Added a download manager with checksum validation and archive extraction support.
- Added tests covering dataset registration, downloads, and extraction flows.

## Phase 4 — Exploratory Analysis (Completed)
- Added reusable summary statistics, metadata summaries, QC reporting, and lightweight visualization helpers.
- Added regression tests for analysis and QC workflows.

## Phase 5 — Preprocessing Pipeline (Completed)
- Added a configurable preprocessing pipeline with filtering, normalization, scaling, feature selection, dimensionality reduction, neighbor-graph construction, and a UMAP-style projection helper.
- Added regression tests for the main preprocessing steps.
