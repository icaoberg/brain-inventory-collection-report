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

    # ─────────────────────────────────────────────
    # Collections Section with Dropdown
    # ─────────────────────────────────────────────
    st.subheader("📁 Collections")
    unique_collections = sorted(df["collection"].dropna().unique())
    selected_collection = st.selectbox("Select a Collection:", unique_collections)
    st.markdown(f"You selected: **{selected_collection}**")

    # ─────────────────────────────────────────────
    # First Histogram: Count of Datasets per Collection
    # ─────────────────────────────────────────────
    st.subheader("📊 Dataset Count per Collection")
    collection_counts = df["collection"].value_counts().sort_index()
    top5_datasets = df["collection"].value_counts().nlargest(5).index.tolist()

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    bars1 = collection_counts.plot(kind="bar", ax=ax1, color="skyblue")

    for i, label in enumerate(collection_counts.index):
        if label in top5_datasets:
            display_label = "Other" if label.lower() in ["other", "count"] else label
            bars1.patches[i].set_color("steelblue")
            bars1.patches[i].set_label(display_label)

    handles1, labels1 = ax1.get_legend_handles_labels()
    by_label1 = dict(zip(labels1, handles1))
    ax1.legend(by_label1.values(), by_label1.keys(), title="Top 5 Collections")

    ax1.set_title("Number of Datasets per Collection")
    ax1.set_xlabel("")
    ax1.set_ylabel("Dataset Count")
    ax1.set_xticklabels([])
    ax1.tick_params(axis="x", bottom=False)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig1)

    # ─────────────────────────────────────────────
    # Second Histogram: Total Number of Files per Collection
    # ─────────────────────────────────────────────
    st.subheader("📦 Total Number of Files per Collection")
    collection_file_counts = df.groupby("collection")["number_of_files"].sum().sort_index()
    top5_files = collection_file_counts.sort_values(ascending=False).head(5).index.tolist()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    bars2 = collection_file_counts.plot(kind="bar", ax=ax2, color="lightcoral")

    for i, label in enumerate(collection_file_counts.index):
        if label in top5_files:
            display_label = "Other" if label.lower() in ["other", "number_of_files"] else label
            bars2.patches[i].set_color("indianred")
            bars2.patches[i].set_label(display_label)

    handles2, labels2 = ax2.get_legend_handles_labels()
    by_label2 = dict(zip(labels2, handles2))
    ax2.legend(by_label2.values(), by_label2.keys(), title="Top 5 Collections")

    ax2.set_title("Total Number of Files per Collection")
    ax2.set_xlabel("")
    ax2.set_ylabel("File Count")
    ax2.set_xticklabels([])
    ax2.tick_params(axis="x", bottom=False)
    ax2.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig2)

except Exception as e:
    st.error(f"Failed to load or process data: {e}")
