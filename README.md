# BioML Workbench

[![CI](https://github.com/AnthonyMorenoSanchez/BioML-Workbench/actions/workflows/ci.yml/badge.svg)](https://github.com/AnthonyMorenoSanchez/BioML-Workbench/actions/workflows/ci.yml)

BioML Workbench is an interactive research-software project for sparse single-cell RNA-seq analysis and reproducible machine-learning workflows.

The current implementation uses the PBMC68k dataset to support barcode-aligned labels, quality control, PCA, UMAP, Leiden clustering, gene-expression exploration, cohort comparison, exploratory differential expression, and held-out classification.

## Project Focus

Single-cell datasets are high-dimensional, sparse, and easy to analyze incorrectly. BioML Workbench is designed to make the analysis workflow inspectable and reproducible by:

- Preserving sparse AnnData matrices during analysis.
- Aligning labels strictly by cell barcode.
- Recording label provenance and preprocessing settings.
- Separating exploratory cell-level comparisons from donor-level biological conclusions.
- Saving models, predictions, metrics, figures, and reports as run artifacts.
- Validating code quality with automated linting, type checks, tests, and CI.

## Current Capabilities

| Area | Functionality |
|---|---|
| Dataset loading | Load and cache PBMC68k as a sparse AnnData object |
| Label management | Align reference or user-uploaded labels by barcode and record provenance |
| Quality control | Calculate counts, detected genes, and mitochondrial-expression metrics |
| Preprocessing | Filter cells and genes, normalize, log transform, select highly variable genes, run PCA, and build a neighbor graph |
| Exploration | Display QC plots, UMAP embeddings, Leiden clusters, cluster sizes, and marker-gene tables |
| Cohort comparison | Define cohorts from labels, clusters, QC thresholds, barcode lists, and gene-expression thresholds |
| Differential expression | Run exploratory cohort-to-cohort Wilcoxon testing with multiple-testing correction and volcano plots |
| Machine learning | Train sparse logistic-regression classifiers with stratified held-out evaluation |
| Reproducibility | Save configurations, cohort definitions, predictions, metrics, figures, models, and Markdown reports |

## Quick Start

Use a virtual environment for all commands.

```powershell
# From the repository root
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev,ui]"
```

Start the Streamlit application:

```powershell
python -m streamlit run ui/streamlit_app.py
```

## PBMC68k Workflow

1. Start the application.
2. Enable **Use PBMC68k sample dataset** in the sidebar.
3. Select **Load PBMC68k**.
4. Open **Preprocessing** and run sparse preprocessing.
5. Explore UMAP embeddings, Leiden clusters, QC metrics, and marker genes.
6. Upload barcode-keyed labels in the **Labels** page when supervised analysis is needed.
7. Define cohorts in **Comparison Explorer**.
8. Compare expression patterns across cohorts.
9. Run exploratory differential expression and export a comparison report.
10. Train a held-out sparse logistic classifier using an aligned label column.

The dataset is cached locally after its first load:

```text
data/cache/pbmc68k/pbmc68k.h5ad
```

The cache and generated artifacts are excluded from version control.

## Label Format

Upload labels as CSV or TSV with:

- A required `barcode` column.
- One or more label columns.

Example:

```text
barcode,cell_type
AAACCTGAGAAACCAT-1,CD14+ Monocyte
AAACCTGAGAAACCGC-1,CD19+ B
```

Labels are aligned by barcode, not row position. Duplicate barcodes are rejected, and unmatched barcodes are reported.

## Cohort Comparison

The **Comparison Explorer** lets users define named cohorts using:

- Aligned cell-type labels.
- Leiden cluster membership.
- Metadata categories.
- QC thresholds.
- Barcode include or exclude lists.
- Gene-expression thresholds.

For example, a cohort can represent:

```text
Leiden clusters 3 and 5
AND
NKG7 expression >= 1.5
AND
mitochondrial percentage < 20
```

Cohorts are stored as reusable rules instead of copying the full cell-by-gene matrix. This keeps comparisons reproducible and avoids unnecessary dense data copies.

## Differential Expression

After defining and running two cohorts, use **Differential Expression** to compare them.

The workflow:

- Performs per-gene two-sided Wilcoxon rank-sum tests.
- Applies Benjamini-Hochberg multiple-testing correction.
- Reports expression summaries and percent-expressing cells.
- Calculates fold-change direction.
- Generates an interactive volcano plot.
- Exports tables, Plotly HTML figures, and a Markdown report.

## Scientific Limitations

PBMC68k contains cells from a single donor.

Cell-level differential-expression results are useful for exploratory comparisons within this dataset, but they do not establish biological generalization across donors, laboratories, chemistries, disease conditions, or populations.

Likewise, random held-out cell splits measure within-dataset predictive performance. They do not measure cross-donor or clinical generalization.

Published reference labels should be interpreted as annotations, not definitive biological ground truth.

## Programmatic Example

```python
from bioml_workbench.dashboard import load_pbmc68k_dataset
from bioml_workbench.single_cell import cluster_cells, preprocess_adata

dataset = load_pbmc68k_dataset()
adata = dataset["adata"]

processed_adata = preprocess_adata(
    adata,
    min_genes=50,
    n_top_genes=2_000,
    n_pcs=50,
    n_neighbors=15,
)

cluster_cells(processed_adata)
print(processed_adata.obs["leiden"].value_counts())
```

## Development Commands

Run the full validation suite before committing changes:

```powershell
ruff check .
black --check .
mypy src
pytest -q
```

## Project Structure

```text
BioML-Workbench/
├── .github/
│   └── workflows/
│       └── ci.yml
├── configs/                      # Runtime configuration
├── src/
│   └── bioml_workbench/
│       ├── data/                 # Dataset loading and label alignment
│       ├── single_cell/          # QC, preprocessing, cohorts, plots, DE, training
│       ├── dashboard.py          # Dataset and AnnData loading helpers
│       └── experiment.py         # Reproducible run artifacts
├── tests/                        # Unit and integration-style tests
├── ui/
│   └── streamlit_app.py          # Interactive Streamlit application
├── pyproject.toml                # Package metadata and tooling configuration
└── README.md
```

## Data Attribution

The PBMC68k dataset is loaded through `scvelo.datasets.pbmc68k()` and originates from the 10x Genomics Fresh 68k PBMCs Donor A dataset.

- Dataset license: CC BY 4.0
- Dataset source: https://www.10xgenomics.com/datasets/fresh-68-k-pbm-cs-donor-a-1-standard-1-1-0
