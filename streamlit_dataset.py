import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
import humanize

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

    # ────────────────────────────────
    # Collection Selection Dropdown
    # ────────────────────────────────
    st.subheader("📁 Collections")
    unique_collections = sorted(df["collection"].dropna().unique())
    default_index = unique_collections.index("26") if "26" in unique_collections else 0
    selected_collection = st.selectbox(
        "Select a Collection:", unique_collections, index=default_index
    )

    # Filter to selected collection
    collection_subset = df[df["collection"] == selected_collection]


except Exception as e:
    st.error(f"Failed to load or process data: {e}")
