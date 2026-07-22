from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from bioml_workbench.dashboard import (
    build_dashboard_payload,
    load_pbmc68k_dataset,
    load_tabular_data,
)
from bioml_workbench.data import attach_labels
from bioml_workbench.experiment import ExperimentRun
from bioml_workbench.single_cell import (
    cluster_cells,
    cluster_size_figure,
    embedding_figure,
    preprocess_adata,
    qc_scatter_figure,
    rank_marker_genes,
    train_classifier,
)

st.set_page_config(page_title="BioML Workbench", layout="wide")

st.title("BioML Workbench")
st.write(
    "Upload a tabular biological dataset to inspect features, "
    "run QC, preprocess it, and train a baseline model."
)

if "payload" not in st.session_state:
    st.session_state.payload = None

pages = [
    "Home",
    "Dataset Explorer",
    "Labels",
    "QC",
    "Preprocessing",
    "Exploration",
    "Training",
    "Evaluation",
]
page = st.sidebar.selectbox("Page", pages)

st.sidebar.caption("Choose a data source")
use_pbmc = st.sidebar.checkbox("Use PBMC68k sample dataset", value=False)

if use_pbmc:
    st.sidebar.caption(
        "The first load downloads and caches " "the sparse dataset locally."
    )
    if st.sidebar.button("Load PBMC68k"):
        try:
            with st.spinner("Loading cached PBMC68k data or downloading it once..."):
                dataset_payload = load_pbmc68k_dataset(cache_dir="data/cache")
                st.session_state.payload = build_dashboard_payload(dataset_payload)
                st.session_state.data_source = "pbmc68k"
        except Exception as exc:  # pragma: no cover - UI error path
            st.sidebar.error(f"Unable to load PBMC68k: {exc}")
    payload = st.session_state.payload
else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload a CSV matrix",
        type=["csv"],
        help="Expected columns: sample, feature_1, feature_2, ...",
    )

    if uploaded_file is not None:
        path = Path(uploaded_file.name)
        path.write_bytes(uploaded_file.getvalue())
        data = load_tabular_data(path)
        payload = build_dashboard_payload(data)
        st.session_state.payload = payload
        st.session_state.data_source = "uploaded_csv"
    else:
        payload = st.session_state.payload

if payload is None:
    st.info("Upload a CSV file to begin analysis.")
    st.stop()

adata = payload.get("adata")

if page == "Home":
    st.header("Welcome")
    st.metric("Samples", payload["summary"]["sample_count"])
    st.metric("Features", payload["summary"]["feature_count"])

if page == "Dataset Explorer":
    st.header("Dataset Explorer")
    st.dataframe(
        {
            "sample": payload["sample_names"],
            "feature_count": [len(payload["feature_names"])]
            * len(payload["sample_names"]),
        }
    )

if page == "Labels":
    st.header("Labels")
    if adata is None:
        st.info("Label alignment is available for loaded AnnData datasets.")
    else:
        label_file = st.file_uploader(
            "Upload barcode-keyed labels", type=["csv", "tsv"]
        )
        if label_file is not None:
            separator = "\t" if label_file.name.endswith(".tsv") else ","
            labels = pd.read_csv(label_file, sep=separator)
            st.dataframe(labels.head())
            label_column = st.selectbox(
                "Label column",
                [column for column in labels.columns if column != "barcode"],
            )
            provenance = st.selectbox(
                "Label provenance",
                ["published_10x_reference", "user_uploaded", "user_edited"],
            )
            if st.button("Align labels by barcode"):
                try:
                    report = attach_labels(
                        adata,
                        labels,
                        label_column=label_column,
                        provenance=provenance,
                    )
                    st.session_state.label_report = report
                    st.success("Labels aligned without reordering cells.")
                    st.json(report)
                except ValueError as exc:
                    st.error(str(exc))

if page == "QC":
    st.header("Quality Control")
    if adata is None:
        qc_report = payload["summary"]["qc_report"]
        st.write(qc_report)
        st.bar_chart({"sample_totals": qc_report["sample_totals"]})
    elif {"total_counts", "n_genes_by_counts"}.issubset(adata.obs.columns):
        st.plotly_chart(qc_scatter_figure(adata), use_container_width=True)
    else:
        st.info("Run single-cell preprocessing to calculate QC metrics.")

if page == "Preprocessing":
    st.header("Preprocessing")
    if adata is None:
        st.write(payload["processed"])
    else:
        min_genes = st.number_input("Minimum detected genes", 0, 10_000, 50)
        n_top_genes = st.number_input("Highly variable genes", 2, 10_000, 2_000)
        n_pcs = st.number_input("PCA components", 2, 100, 50)
        n_neighbors = st.number_input("Neighbors", 2, 100, 15)
        if st.button("Run sparse preprocessing"):
            with st.spinner("Calculating QC, PCA, neighbors, and UMAP..."):
                processed_adata = preprocess_adata(
                    adata,
                    min_genes=int(min_genes),
                    n_top_genes=int(n_top_genes),
                    n_pcs=int(n_pcs),
                    n_neighbors=int(n_neighbors),
                )
                cluster_cells(processed_adata)
                st.session_state.payload["adata"] = processed_adata
            st.success("Preprocessing and Leiden clustering completed.")

if page == "Exploration":
    st.header("Exploration")
    if adata is None or "X_umap" not in adata.obsm:
        st.info("Run sparse preprocessing before exploring embeddings.")
    else:
        color_options = list(adata.obs.columns)
        color_by = st.selectbox(
            "Color UMAP by", color_options, index=color_options.index("leiden")
        )
        st.plotly_chart(
            embedding_figure(adata, color_by=color_by), use_container_width=True
        )
        st.plotly_chart(cluster_size_figure(adata), use_container_width=True)
        if st.button("Rank marker genes"):
            st.dataframe(rank_marker_genes(adata))

if page == "Training":
    st.header("Training")
    if adata is None:
        st.info("Load an AnnData dataset and upload labels before supervised training.")
    else:
        label_columns = [
            column for column in adata.obs.columns if adata.obs[column].notna().any()
        ]
        if not label_columns:
            st.info("Upload and align barcode-keyed labels before supervised training.")
        else:
            label_column = st.selectbox("Training target", label_columns)
            test_size = st.slider("Held-out test fraction", 0.1, 0.5, 0.2)
            if st.button("Train held-out logistic classifier"):
                try:
                    run = ExperimentRun.create(
                        "artifacts", st.session_state.data_source
                    )
                    run.log_config(
                        {
                            "label_column": label_column,
                            "test_size": test_size,
                            "data_source": st.session_state.data_source,
                        }
                    )
                    result = train_classifier(
                        adata,
                        label_column=label_column,
                        output_dir=run.path,
                        test_size=test_size,
                    )
                    run.log_metrics(result["metrics"])
                    st.session_state.training_result = result
                    st.json(result["metrics"])
                except ValueError as exc:
                    st.error(str(exc))

if page == "Evaluation":
    st.header("Held-out Evaluation")
    result = st.session_state.get("training_result")
    if result is None:
        st.info("Run a held-out training job to inspect predictions and metrics.")
    else:
        st.json(result["metrics"])
        st.dataframe(result["predictions"])
        st.caption("Artifacts: " + ", ".join(result["artifacts"]))
