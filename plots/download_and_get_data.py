import streamlit as st
import plotly.express as px
import requests
import pandas as pd
import re
from datetime import datetime
import humanize


def load_data():
    URL = "https://download.brainimagelibrary.org/inventory/daily/reports/today.json"
    st.caption(f"Loading data from: {URL}")

    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)

    df["collection"] = df["bildirectory"].apply(extract_collection)

    # Convert raw size to human-readable format
    df["pretty_size"] = df["size"].apply(
        lambda s: humanize.naturalsize(s, binary=True) if pd.notnull(s) else None
    )

    # Sort for preview table
    df_sorted = df.sort_values(by="number_of_files", ascending=False)

    # Preview table of key metadata
    preview_df = df_sorted[
        ["collection", "bildid", "number_of_files", "pretty_size"]
    ].rename(
        columns={
            "collection": "Collection",
            "bildid": "Brain ID",
            "number_of_files": "Number of Files",
            "pretty_size": "Size",
        }
    )

    return df_sorted


# Extract 2-character collection code from bildirectory
def extract_collection(path):
    match = re.search(r"/bil/data/([a-f0-9]{2})/", path)
    return match.group(1) if match else None
