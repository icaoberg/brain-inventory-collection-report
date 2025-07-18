import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
import humanize

# Import modular plotting functions
from plots.collection.affiliation import plot as affiliation_plot
from plots.download_get_data import load_data
from plots.intro import print_intro

from plots.contributor import plot_contributor_pie as load_data
from plots.file_distribution import plot_file_distribution_bar
from plots.mime_type import plot_mime_pie

# Load and preprocess data (simplified for demo)
# ...

# Dropdown
selected_collection = st.selectbox("Select collection", df["collection"].dropna().unique())

# Call plotting functions

plot_contributor_pie(df, selected_collection)
plot_file_distribution_bar(df, selected_collection)
plot_mime_pie(df)


# ────────────────────────────────
# App Title and Introduction
# ────────────────────────────────
print_intro()

try:
    # ────────────────────────────────
    # Load and Parse JSON Data
    # ────────────────────────────────
    df = load_data()

    st.subheader("Sorted by Number of Files (Descending)")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ────────────────────────────────
    # Collection Selection Dropdown
    # ────────────────────────────────
    st.subheader("📁 Collections")
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
    # Pie Chart: Dataset by Affiliation
    # ────────────────────────────────
    affiliation_plot(df, selected_collection)

    # ────────────────────────────────
    # Bar Chart: Dataset Count by Collection (Labeled by bildid)
    # ────────────────────────────────
    st.subheader("📈 File Distribution in Selected Collection")

    # Filter datasets to selected collection
    bar_df = df[df["collection"] == selected_collection][
        ["collection", "bildid"]
    ].copy()
    bar_df["count"] = 1  # Each dataset contributes one count

    # Create labeled bar chart
    fig_bar = px.bar(
        bar_df,
        x="collection",
        y="count",
        text="bildid",
        hover_data={"bildid": True, "collection": False, "count": False},
        title="Number of Datasets per Collection",
        labels={"count": "Dataset", "collection": "Collection"},
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(
        showlegend=False,
        xaxis=dict(tickangle=45),
        yaxis=dict(gridcolor="lightgray"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ────────────────────────────────
    # Pie Chart: File Types
    # ────────────────────────────────
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

    # ────────────────────────────────
    # Pie Chart: MIME Types
    # ────────────────────────────────
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
