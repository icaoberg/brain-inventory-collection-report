import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
import humanize
import matplotlib.pyplot as plt
import plotly.express as px

# App Title
st.title("🧠 Brain Image Library Inventory Report")

# Introduction
st.markdown(
    """
The **Brain Image Library (BIL)** is a national public resource that supports the storage, sharing, and analysis of large-scale brain imaging datasets. 
This report provides a snapshot of the current dataset inventory, highlighting key metadata including file counts, sizes, and organizational structure.
"""
)

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

    def extract_collection(path):
        match = re.search(r"/bil/data/([a-f0-9]{2})/", path)
        return match.group(1) if match else None

    df["collection"] = df["bildirectory"].apply(extract_collection)
    df["pretty_size"] = df["size"].apply(
        lambda s: humanize.naturalsize(s, binary=True) if pd.notnull(s) else None
    )
    df_sorted = df.sort_values(by="number_of_files", ascending=False)

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

    st.subheader("Preview: Sorted by Number of Files (Descending)")
    st.dataframe(preview_df, use_container_width=True, hide_index=True)

    # Collections
    st.subheader("📁 Collections")
    unique_collections = sorted(df["collection"].dropna().unique())
    default_index = unique_collections.index("26") if "26" in unique_collections else 0
    selected_collection = st.selectbox(
        "Select a Collection:", unique_collections, index=default_index
    )

    st.markdown(f"You selected: **{selected_collection}**")

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

    st.subheader("🏛️ Dataset Distribution by Affiliation (Selected Collection)")
    collection_subset = df[df["collection"] == selected_collection]

    if (
        "affiliation" in collection_subset.columns
        and collection_subset["affiliation"].notna().sum() > 0
    ):
        affiliation_counts = collection_subset["affiliation"].dropna().value_counts()
        fig_aff = px.pie(
            names=affiliation_counts.index,
            values=affiliation_counts.values,
            title="Affiliations in Selected Collection",
        )
        st.plotly_chart(fig_aff, use_container_width=True)
    else:
        st.info("No affiliation information is present for the selected collection.")

    st.subheader("📈 File Distribution in Selected Collection")

    # Filter to selected collection only
    bar_df = df[df["collection"] == selected_collection][
        ["collection", "bildid"]
    ].copy()
    bar_df["count"] = 1  # Each dataset contributes one count

    # Create the bar chart and label each bar with its bildid
    fig_bar = px.bar(
        bar_df,
        x="collection",
        y="count",
        text="bildid",  # Add the label
        hover_data={"bildid": True, "collection": False, "count": False},
        title="Number of Datasets per Collection",
        labels={"count": "Dataset", "collection": "Collection"},
    )

    fig_bar.update_traces(textposition="outside")  # Position labels above bars
    fig_bar.update_layout(
        showlegend=False, xaxis=dict(tickangle=45), yaxis=dict(gridcolor="lightgray")
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("📈 File Distribution in Selected Collection")

    # Filter to selected collection only
    bar_df = df[df["collection"] == selected_collection][
        ["collection", "bildid"]
    ].copy()
    bar_df["count"] = 1  # Each dataset contributes one count

    # Create the bar chart and label each bar with its bildid
    fig_bar = px.bar(
        bar_df,
        x="collection",
        y="count",
        text="bildid",  # Add the label
        hover_data={"bildid": True, "collection": False, "count": False},
        title="Number of Datasets per Collection",
        labels={"count": "Dataset", "collection": "Collection"},
    )

    fig_bar.update_traces(textposition="outside")  # Position labels above bars
    fig_bar.update_layout(
        showlegend=False, xaxis=dict(tickangle=45), yaxis=dict(gridcolor="lightgray")
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # File Types Pie Chart
    st.subheader("🗂️ File Types Distribution")
    if "file_types" in df.columns and df["file_types"].notna().sum() > 0:
        filetype_counts = df["file_types"].dropna().value_counts()
        fig4, ax4 = plt.subplots(figsize=(6, 6))
        wedges, _, _ = ax4.pie(
            filetype_counts, labels=None, autopct="%1.1f%%", startangle=140
        )
        ax4.axis("equal")
        ax4.set_title("File Type Breakdown")
        ax4.legend(
            wedges,
            filetype_counts.index,
            title="File Types",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize="small",
        )
        st.pyplot(fig4)
    else:
        st.info("No file-type information is present.")

    # MIME Types Pie Chart
    st.subheader("📄 MIME Types Distribution")
    if "mime_types" in df.columns and df["mime_types"].notna().sum() > 0:
        mime_counts = df["mime_types"].dropna().value_counts()
        fig5, ax5 = plt.subplots(figsize=(6, 6))
        wedges, _, _ = ax5.pie(
            mime_counts, labels=None, autopct="%1.1f%%", startangle=140
        )
        ax5.axis("equal")
        ax5.set_title("MIME Type Breakdown")
        ax5.legend(
            wedges,
            mime_counts.index,
            title="MIME Types",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize="small",
        )
        st.pyplot(fig5)
    else:
        st.info("No MIME-type information is present.")

except Exception as e:
    st.error(f"Failed to load or process data: {e}")
