# Phase F - Held-Out Supervised Evaluation

`train_classifier` trains a sparse logistic-regression baseline only from an explicitly selected, barcode-aligned label column. It uses a stratified cell-level holdout, saves test predictions and maximum probabilities, and persists model, metrics, and manifest artifacts.

This is not cross-donor validation. PBMC68k is a single-donor reference dataset, so held-out results must be interpreted as within-dataset performance.