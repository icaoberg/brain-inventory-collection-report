import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
import humanize
import matplotlib.pyplot as plt

# App Title
st.title("🧠 Brain Image Library Inventory Report")

# Introduction
st.markdown("""
The **Brain Image Library (BIL)** is a national public resource that supports the storage, sharing, and analysis of large-scale brain imaging datasets. 
This report provides a snapshot of the current dataset inventory, highlighting key metadata including file counts, sizes, and organizational structure.
""")

# Subtitle with today's date
today_str = datetime.today().strftime("%B %d, %Y")
st.markdown(f"### 📅 Report Date: {today_str}")

# Load data
URL = "https://download.brainimagelibrary.org//inventory/daily/reports/today.json"
st.caption(f"Loading data from: {URL}")

try:
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)

    # Extract collection from bildirectory
    def extract_collection(path):
        match = re.search(r"/bil/data/([a-f0-9]{2})/", path)
        return match.group(1) if match else None

    df["collection"] = df["bildirectory"].apply(extract_collection)

    # Compute pretty_size from size
    df["pretty_size"] = df["size"].apply(lambda s: humanize.naturalsize(s, binary=True) if pd.notnull(s) else None)

    # Sort by number_of_files in descending order
    df_sorted = df.sort_values(by="number_of_files", ascending=False)

    # Select and rename columns for display
    preview_df = df_sorted[["collection", "bildid", "number_of_files", "pretty_size"]].rename(columns={
        "collection": "Collection",
        "bildid": "Brain ID",
        "number_of_files": "Number of Files",
        "pretty_size": "Size"
    })

    # Display table preview without index
    st.subheader("Preview: Sorted by Number of Files (Descending)")
    st.dataframe(preview_df, use_container_width=True, hide_index=True)

    # Plot histogram of collection counts
    st.subheader("📊 Dataset Count per Collection")
    collection_counts = df["collection"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    collection_counts.plot(kind="bar", ax=ax)
    ax.set_title("Number of Datasets per Collection")
    ax.set_xlabel("Collection")
    ax.set_ylabel("Dataset Count")
    ax.tick_params(axis="x", rotation=90)  # Rotate labels vertically
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

except Exception as e:
    st.error(f"Failed to load or process data: {e}")
