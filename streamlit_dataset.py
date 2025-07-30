import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
import humanize

from plots.download_and_get_data import load_collection_data
from plots.download_and_get_data import load_dataset_data
from plots.intro import print_dataset_intro as print_intro
from plots.datasets import plot_extension_histogram

# ────────────────────────────────
# App Title and Introduction
# ────────────────────────────────
print_intro()

try:
    # ────────────────────────────────
    # Load and Parse JSON Data
    # ────────────────────────────────
    df = load_collection_data()

    # ────────────────────────────────
    # Collection Selection in Sidebar
    # ────────────────────────────────
    st.sidebar.header("📁 Collections")
    unique_collections = sorted(df["collection"].dropna().unique())
    default_index = unique_collections.index("26") if "26" in unique_collections else 0
    selected_collection = st.sidebar.selectbox(
        "Select a Collection", unique_collections, index=default_index
    )

    # Filter to selected collection
    collection_subset = df[df["collection"] == selected_collection]

    # ────────────────────────────────
    # BILD ID Selection in Sidebar
    # ────────────────────────────────
    st.sidebar.markdown("### 📌 Datasets in Collection")
    matching_bildids = sorted(collection_subset["bildid"].dropna().unique())
    selected_bildid = st.sidebar.selectbox(
        "Select a Dataset (BILD ID)", matching_bildids
    )

    data = load_dataset_data(selected_bildid)
    
    st.write(f'Metadata version: {data["version"]}')
    st.write(f'General modality: {data["modality"]}')
    st.write(f'Technique: {data["technique"]}')

    if "manifest" in data:
        manifest_df = pd.DataFrame(data["manifest"])
        st.write("📄 Manifest DataFrame")
        st.dataframe(manifest_df)
        plot_extension_histogram(df)
    else:
        st.warning("The 'manifest' key was not found in the JSON block.")
except Exception as e:
    st.error(f"Failed to load or process data: {e}")