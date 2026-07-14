# Changelog

## [0.1.0] - 2026-07-14

### Added
- Initial Python package scaffold for BioML Workbench.
- YAML-driven configuration and logging foundations.
- GitHub Actions CI workflow and pre-commit hooks.
- Docker and Makefile-based development workflow.
- Unit tests covering configuration and logging behavior.

## [0.2.0] - 2026-07-14

### Added
- Extended configuration system with dataset, training, and dashboard settings.
- Environment variable overrides via the `BIOML_` prefix.
- Config path resolution with `BIOML_CONFIG_PATH`.
- CLI support for showing resolved configuration.

## [0.3.0] - 2026-07-14

### Added
- Core utility modules for file management, caching, timing, and reproducible seeding.
- Reusable exception classes and logging-aware exception handling.
- Configuration manager for reloadable runtime configuration.
