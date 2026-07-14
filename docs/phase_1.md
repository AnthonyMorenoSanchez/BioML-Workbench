# Phase 1 — Configuration System

Phase 1 extends configuration support across the repository.

## Completed work

- Added `dataset`, `training`, and `dashboard` configuration sections.
- Implemented environment variable overrides using the `BIOML_` prefix.
- Added support for overriding the config file location with `BIOML_CONFIG_PATH`.
- Updated CLI to print the full resolved configuration.
- Added tests for YAML loading, environment overrides, and config path resolution.
- Updated documentation and roadmap metadata.

## Behavior

- Built-in config files under `configs/` resolve relative resource paths against the repository root.
- Custom config files resolve relative paths against the config file location.
