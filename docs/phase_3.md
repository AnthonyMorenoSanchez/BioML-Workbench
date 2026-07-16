# Phase 3 — Data Engineering

Phase 3 introduces the first dataset-oriented infrastructure for the BioML Workbench.

## Completed work

- Added a dataset registry for known datasets and metadata lookup.
- Added a download manager capable of copying local files, fetching remote artifacts, and validating checksums.
- Added archive extraction support for ZIP and TAR.GZ datasets.
- Added tests covering registry lookups, checksum validation, and archive extraction.

## Usage

```python
from bioml_workbench.data import DatasetMetadata, DatasetRegistry, DownloadManager

registry = DatasetRegistry()
registry.register(
    DatasetMetadata(
        name="pbmc68k",
        description="PBMC68k sample dataset",
        source="https://example.com/pbmc68k.csv",
        checksum="abc123",
    )
)

manager = DownloadManager(cache_dir="data/cache")
manager.download(registry.get("pbmc68k"), destination="data/raw/pbmc68k.csv")
```

## Next phase

The next implementation milestone is Phase 4 — Exploratory Analysis, which will focus on summary statistics, distributions, QC reports, and visualization support.
