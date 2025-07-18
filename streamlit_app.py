
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

    def extract_collection(path):
        match = re.search(r"/bil/data/([a-f0-9]{2})/", path)
        return match.group(1) if match else None

    df["collection"] = df["bildirectory"].apply(extract_collection)
    df["pretty_size"] = df["size"].apply(lambda s: humanize.naturalsize(s, binary=True) if pd.notnull(s) else None)
    df_sorted = df.sort_values(by="number_of_files", ascending=False)

    preview_df = df_sorted[["collection", "bildid", "number_of_files", "pretty_size"]].rename(columns={
        "collection": "Collection",
        "bildid": "Brain ID",
        "number_of_files": "Number of Files",
        "pretty_size": "Size"
    })

    st.subheader("Preview: Sorted by Number of Files (Descending)")
    st.dataframe(preview_df, use_container_width=True, hide_index=True)

    # Collections
    st.subheader("📁 Collections")
    unique_collections = sorted(df["collection"].dropna().unique())
    selected_collection = st.selectbox("Select a Collection:", unique_collections)
    st.markdown(f"You selected: **{selected_collection}**")

    filtered_df = df[df["collection"] == selected_collection][["collection", "bildid", "number_of_files", "pretty_size"]].rename(columns={
        "collection": "Collection",
        "bildid": "Brain ID",
        "number_of_files": "Number of Files",
        "pretty_size": "Size"
    })
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # Pie chart: number_of_files per dataset
    st.subheader("📈 File Distribution in Selected Collection")
    pie_data = df[df["collection"] == selected_collection].set_index("bildid")["number_of_files"]
    pie_data = pie_data[pie_data > 0].sort_values(ascending=False)

    fig3, ax3 = plt.subplots(figsize=(6, 6))
    wedges, _, _ = ax3.pie(pie_data, labels=None, autopct="%1.1f%%", startangle=140)
    ax3.axis("equal")
    ax3.set_title("Number of Files per Dataset")
    labels = list(pie_data.index)
    num_cols = (len(labels) - 1) // 25 + 1
    ax3.legend(wedges, labels, title="Brain ID", loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small", ncol=num_cols)
    st.pyplot(fig3)


    # ─────────────────────────────────────────────
    # Affiliation Pie Chart
    st.subheader("🏛️ Dataset Distribution by Affiliation (Selected Collection)")
    affiliation_subset = df[df["collection"] == selected_collection]
    if "affiliation" in affiliation_subset.columns and affiliation_subset["affiliation"].notna().sum() > 0:
        affiliation_counts = affiliation_subset["affiliation"].dropna().value_counts()
        fig_aff, ax_aff = plt.subplots(figsize=(6, 6))
        wedges, _, _ = ax_aff.pie(affiliation_counts, labels=None, autopct="%1.1f%%", startangle=140)
        ax_aff.axis("equal")
        ax_aff.set_title("Affiliation Breakdown (Selected Collection)")
        ax_aff.legend(wedges, affiliation_counts.index, title="Affiliations", loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small")
        st.pyplot(fig_aff)
    else:
        st.info("No affiliation information is present for the selected collection.")

    # ─────────────────────────────────────────────
    # General Modality Pie Chart
    # ─────────────────────────────────────────────
    st.subheader("🧪 Dataset Distribution by General Modality")
    if "general_modality" in df.columns and df["general_modality"].notna().sum() > 0:
        modality_counts = df["general_modality"].dropna().value_counts()
        fig_mod, ax_mod = plt.subplots(figsize=(6, 6))
        wedges, _, _ = ax_mod.pie(modality_counts, labels=None, autopct="%1.1f%%", startangle=140)
        ax_mod.axis("equal")
        ax_mod.set_title("Dataset Count by General Modality")
        ax_mod.legend(wedges, modality_counts.index, title="General Modality", loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small")
        st.pyplot(fig_mod)
    else:
        st.info("No general modality information is present.")
    # File Types Pie Chart
    st.subheader("🗂️ File Types Distribution")
    if "file_types" in df.columns and df["file_types"].notna().sum() > 0:
        filetype_counts = df["file_types"].dropna().value_counts()
        fig4, ax4 = plt.subplots(figsize=(6, 6))
        wedges, _, _ = ax4.pie(filetype_counts, labels=None, autopct="%1.1f%%", startangle=140)
        ax4.axis("equal")
        ax4.set_title("File Type Breakdown")
        ax4.legend(wedges, filetype_counts.index, title="File Types", loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small")
        st.pyplot(fig4)
    else:
        st.info("No file-type information is present.")

    # MIME Types Pie Chart
    st.subheader("📄 MIME Types Distribution")
    if "mime_types" in df.columns and df["mime_types"].notna().sum() > 0:
        mime_counts = df["mime_types"].dropna().value_counts()
        fig5, ax5 = plt.subplots(figsize=(6, 6))
        wedges, _, _ = ax5.pie(mime_counts, labels=None, autopct="%1.1f%%", startangle=140)
        ax5.axis("equal")
        ax5.set_title("MIME Type Breakdown")
        ax5.legend(wedges, mime_counts.index, title="MIME Types", loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small")
        st.pyplot(fig5)
    else:
        st.info("No MIME-type information is present.")

    # Frequencies Pie Chart
    st.subheader("📁 File Extension Frequencies")
    if "frequencies" in df.columns and df["frequencies"].notna().sum() > 0:
        all_freqs = df["frequencies"].dropna().tolist()
        freq_total = {}
        for freq_dict in all_freqs:
            if isinstance(freq_dict, dict):
                for ext, count in freq_dict.items():
                    freq_total[ext] = freq_total.get(ext, 0) + count
        if freq_total:
            freq_series = pd.Series(freq_total).sort_values(ascending=False)
            fig6, ax6 = plt.subplots(figsize=(6, 6))
            wedges, _, _ = ax6.pie(freq_series, labels=None, autopct="%1.1f%%", startangle=140)
            ax6.axis("equal")
            ax6.set_title("File Extension Frequency Distribution")
            ax6.legend(wedges, freq_series.index, title="Extensions", loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small")
            st.pyplot(fig6)
        else:
            st.info("No valid frequency data found.")
    else:
        st.info("No file extension frequency information is present.")

except Exception as e:
    st.error(f"Failed to load or process data: {e}")

    # ─────────────────────────────────────────────
    # Statistics for Selected Collection
    # ─────────────────────────────────────────────
    st.subheader("📊 Collection Statistics")

    # Number of datasets (rows) in the selected collection
    num_datasets = filtered_df.shape[0]
    st.markdown(f"**Number of Datasets:** {num_datasets}")

    # Metadata version frequencies
    if "metadata" in df.columns:
        meta_counts = df[df["collection"] == selected_collection]["metadata"].value_counts().to_dict()
        st.markdown("**Metadata Version Frequency:**")
        st.json(meta_counts)
    else:
        st.info("No metadata information is present.")
