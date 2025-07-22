import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
import humanize

# Import modular plotting functions
from plots.collection.affiliation import plot as affiliation_plot
from plots.collection.contributors import plot as contributors_plot
from plots.download_and_get_data import load_data
from plots.intro import print_intro


# ────────────────────────────────
# App Title and Introduction
# ────────────────────────────────
print_intro()

try:
    # ────────────────────────────────
    # Load and Parse JSON Data
    # ────────────────────────────────
    df = load_data()

    st.subheader("Sorted by Number of Files")
    st.dataframe(
        df[
            [
                "metadata_version",
                "bildid",
                "generalmodality",
                "technique",
                "number_of_files",
                "frequencies",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    # ────────────────────────────────
    # Collection Selection Dropdown
    # ────────────────────────────────
    st.subheader("📁 Collections")
    # selected_collection = st.selectbox("Select collection", df["collection"].dropna().unique())
    unique_collections = sorted(df["collection"].dropna().unique())
    default_index = unique_collections.index("26") if "26" in unique_collections else 0
    selected_collection = st.selectbox(
        "Select a Collection:", unique_collections, index=default_index
    )
    st.markdown(f"You selected: **{selected_collection}**")

    # Table of datasets for selected collection
    filtered_df = df[df["collection"] == selected_collection][
        ["collection", "bildid", "number_of_files", "pretty_size"]
    ].rename(
        columns={
            "collection": "Collection",
            "bildid": "Brain ID",
            "number_of_files": "Number of Files",
            "pretty_size": "Size",
        }
    )
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # ────────────────────────────────
    # Pie Chart: Dataset by Affiliation and Contributors
    # ────────────────────────────────
    affiliation_plot(df, selected_collection)
    contributors_plot(df, selected_collection)

    # ────────────────────────────────
    # Bar Chart: Dataset Count by Collection (Labeled by bildid)
    # ────────────────────────────────

    # ────────────────────────────────
    # Pie Chart: File Types
    # ────────────────────────────────

    # ────────────────────────────────
    # Pie Chart: MIME Types
    # ────────────────────────────────

except Exception as e:
    st.error(f"Failed to load or process data: {e}")
