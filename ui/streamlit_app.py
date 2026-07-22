from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

from bioml_workbench.dashboard import (
    build_dashboard_payload,
    load_pbmc68k_dataset,
    load_tabular_data,
)
from bioml_workbench.experiment import ExperimentTracker
from bioml_workbench.workflow import TrainingWorkflow

st.set_page_config(page_title="BioML Workbench", layout="wide")

st.title("BioML Workbench")
st.write("Upload a tabular biological dataset to inspect features, run QC, preprocess it, and train a baseline model.")

if "payload" not in st.session_state:
    st.session_state.payload = None

pages = [
    "Home",
    "Dataset Explorer",
    "QC",
    "Preprocessing",
    "Training",
    "Experiment Browser",
    "Benchmark",
]
page = st.sidebar.selectbox("Page", pages)

st.sidebar.caption("Choose a data source")
use_pbmc = st.sidebar.checkbox("Use PBMC68k sample dataset", value=False)

if use_pbmc:
    st.sidebar.caption("The first load downloads and caches the sparse dataset locally.")
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

if page == "Home":
    st.header("Welcome")
    st.metric("Samples", payload["summary"]["sample_count"])
    st.metric("Features", payload["summary"]["feature_count"])

if page == "Dataset Explorer":
    st.header("Dataset Explorer")
    st.dataframe(
        {
            "sample": payload["sample_names"],
            "feature_count": [len(payload["feature_names"])] * len(payload["sample_names"]),
        }
    )

if page == "QC":
    st.header("Quality Control")
    qc_report = payload["summary"]["qc_report"]
    st.write(qc_report)
    st.bar_chart({"sample_totals": qc_report["sample_totals"]})

if page == "Preprocessing":
    st.header("Preprocessing")
    st.write(payload["processed"])

if page == "Training":
    st.header("Training")
    matrix = payload["processed"]["matrix"]
    labels = [0, 1] * ((len(matrix) + 1) // 2)
    labels = labels[: len(matrix)]
    workflow = TrainingWorkflow(output_dir="artifacts")
    result = workflow.run(matrix, labels, model_name="simple_logistic")
    st.write(result["metrics"])

if page == "Experiment Browser":
    st.header("Experiment Browser")
    tracker = ExperimentTracker(run_name="streamlit-demo")
    tracker.log_metrics({"samples": payload["summary"]["sample_count"]})
    st.write("Logged metrics to the experiment tracker.")

if page == "Benchmark":
    st.header("Benchmark Dashboard")
    st.write(payload["summaries"])
    for feature_name, histogram in payload["histograms"].items():
        st.subheader(feature_name)
        st.bar_chart(histogram)
