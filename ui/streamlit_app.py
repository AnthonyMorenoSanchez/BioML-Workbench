# Minimal Streamlit dashboard skeleton for Phase 8

import streamlit as st

st.set_page_config(page_title="BioML Workbench", layout="wide")

st.title("BioML Workbench")

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

if page == "Home":
    st.header("Welcome to the BioML Workbench")
    st.write("Use the sidebar to navigate to pages.")

if page == "Dataset Explorer":
    st.header("Dataset Explorer")
    st.write("Dataset listing and metadata will appear here.")

if page == "QC":
    st.header("Quality Control")
    st.write("QC reports and filters")

if page == "Preprocessing":
    st.header("Preprocessing")
    st.write("Run preprocessing pipelines from this page.")

if page == "Training":
    st.header("Training")
    st.write("Train models and inspect logs.")

if page == "Experiment Browser":
    st.header("Experiment Browser")
    st.write("Browse experiment artifacts and metrics.")

if page == "Benchmark":
    st.header("Benchmark Dashboard")
    st.write("Run benchmarks and view results.")
