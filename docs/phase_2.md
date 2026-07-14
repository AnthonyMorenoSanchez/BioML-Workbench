# Phase 2 — Core Utilities

Phase 2 implements reusable infrastructure modules that support the rest of the BioML Workbench platform.

## Completed work

- Added a file manager for safe, path-aware file operations.
- Added a disk-backed cache manager with JSON artifact support.
- Added timing utilities for method and context measurement.
- Added a seed manager for reproducible random operations.
- Added exception classes and a logging-aware exception capture context.
- Added a configuration manager for reloadable runtime configuration.

## Usage

```python
from bioml_workbench import FileManager, CacheManager, SeedManager, ConfigurationManager

file_manager = FileManager("data")
file_manager.write_text("example.txt", "hello")

cache_manager = CacheManager("cache")
cache_manager.save("metrics", {"accuracy": 0.98})

seed_manager = SeedManager(seed=1234)
seed_manager.apply()

config_manager = ConfigurationManager()
print(config_manager.get().app_name)
```
