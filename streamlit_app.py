import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
import humanize

# Import modular plotting functions
from plots.collection.affiliation import plot as affiliation_plot
from plots.collection.contributors import plot as contributors_plot
from plots.collection.modalities import plot as generalmodalities_plot
from plots.collection.techniques import plot as techniques_plot

from plots.download_and_get_data import load_collection_data as load_data
from plots.intro import print_collection_intro as print_intro

# ────────────────────────────────
# App Title and Introduction
# ────────────────────────────────
print_intro()

try:
    # ────────────────────────────────
    # Load and Parse JSON Data
    # ────────────────────────────────
    df = load_data()
    df["size"] = df["size"] / (1024**3)

    st.subheader("Sorted by Number of Files")
    st.dataframe(
        df[
            [
                "metadata_version",
                "bildid",
                "generalmodality",
                "technique",
                "number_of_files",
                "size",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    # ────────────────────────────────
    # Collection Selection Dropdown
    # ────────────────────────────────
    st.subheader("📁 Submissions")
    unique_collections = sorted(df["collection"].dropna().unique())
    default_index = unique_collections.index("26") if "26" in unique_collections else 0
    selected_collection = st.selectbox(
        "Select a Collection:", unique_collections, index=default_index
    )

    # Filter to selected collection
    collection_subset = df[df["collection"] == selected_collection]

    st.subheader("📊 Summary")

    # Compute values
    num_datasets = len(collection_subset)
    total_files = collection_subset["number_of_files"].fillna(0).sum() if "number_of_files" in collection_subset.columns else 0
    total_size_bytes = collection_subset["size"].fillna(0).sum() if "size" in collection_subset.columns else 0
    readable_size = humanize.naturalsize(total_size_bytes, binary=True)

    avg_score = collection_subset["score"].dropna().mean() if "score" in collection_subset.columns else None
    coverage_pct = f"{avg_score * 1:.2f}%" if pd.notna(avg_score) else "N/A"

    # Display as bullet points
    st.markdown(f"""
    - **Total number of datasets:** {num_datasets:,}
    - **Total number of files:** {int(total_files):,}
    - **Total size of collection:** {readable_size}
    - **Total checksum coverage:** {coverage_pct}
    """)

    # ────────────────────────────────
    # Dataset by Affiliation and Contributors
    # ────────────────────────────────
    affiliation_plot(df, selected_collection)

    # ────────────────────────────────
    # Dataset by Modalities and Techniques
    # ────────────────────────────────
    techniques_plot(df, selected_collection)

except Exception as e:
    st.error(f"Failed to load or process data: {e}")
