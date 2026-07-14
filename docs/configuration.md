# Configuration

BioML Workbench uses YAML configuration files and environment variable overrides to keep runtime behavior flexible and reproducible.

## Default configuration file

The default configuration lives in `configs/default.yaml` and includes the following sections:

- `app_name`
- `logging`
- `dataset`
- `training`
- `dashboard`

Example:

```yaml
app_name: bioml-workbench
logging:
  level: INFO
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  to_file: false
  file_path: logs/bioml_workbench.log

dataset:
  name: pbmc68k
  source: pbmc68k
  raw_data_path: data/raw
  processed_data_path: data/processed
  cache_path: data/cache
  download_url: ""
  checksum: ""

training:
  random_seed: 42
  model_type: random_forest
  batch_size: 128
  learning_rate: 0.001
  max_epochs: 10
  checkpoint_path: artifacts/checkpoints
  experiment_name: default

dashboard:
  enabled: true
  host: 127.0.0.1
  port: 8000
  title: BioML Workbench Dashboard
```

## Environment variable overrides

Environment variables beginning with `BIOML_` can override YAML fields. Nested keys are separated with double underscores (`__`).

Example: `BIOML_TRAINING__BATCH_SIZE=256`

Path resolution

Built-in configuration files under `configs/` resolve relative paths against the repository root.
Custom config files resolve relative paths against the config file location.

Examples:

```bash
export BIOML_TRAINING__BATCH_SIZE=256
export BIOML_DASHBOARD__ENABLED=false
export BIOML_DATASET__NAME=pbmc68k-test
```

## Config path override

Set `BIOML_CONFIG_PATH` to point to a YAML config file when you want to use a different configuration source.

```bash
export BIOML_CONFIG_PATH=configs/production.yaml
```

## CLI support

Use the CLI to inspect the resolved configuration:

```bash
python -m bioml_workbench --show-config
```
