# Phase E - Interactive Single-Cell Figures

The plotting layer uses Plotly and the AnnData analysis state produced in Phase D. It provides QC scatter plots, UMAP embeddings colored by observation metadata, and cluster-size bar charts. Marker-gene ranking is available for Leiden clusters through Scanpy.

Figures operate on AnnData embeddings and metadata; they do not densify the full expression matrix.