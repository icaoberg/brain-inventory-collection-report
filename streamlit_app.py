import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
import humanize

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

    # Sort by number_of_files in ascending order
    df_sorted = df.sort_values(by="number_of_files", ascending=True)

    # Select and rename columns for display
    preview_df = df_sorted[["collection", "bildid", "number_of_files", "pretty_size"]].rename(columns={
        "collection": "Collection",
        "bildid": "DID",
        "number_of_files": "Number of Files",
        "pretty_size": "Size"
    })

    # Display table preview without index
    st.subheader("Preview: Sorted by Number of Files (Ascending)")
    st.dataframe(preview_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Failed to load or process data: {e}")