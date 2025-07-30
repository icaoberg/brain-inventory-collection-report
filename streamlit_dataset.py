import streamlit as st
import pandas as pd

from plots.download_and_get_data import load_collection_data, load_dataset_data
from plots.intro import print_dataset_intro as print_intro
import plotly.express as px

def plot_checksum_sunburst_from_df(df: pd.DataFrame):
    """
    Plot a sunburst chart using aggregated checksum scores from a DataFrame.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the columns:
                         'score', 'md5', 'sha256', 'xxh64sum', and 'b2sum'
    """
    required_cols = {"score", "md5", "sha256", "xxh64", "b2sum"}
    if not required_cols.issubset(df.columns):
        st.error(f"DataFrame must contain columns: {', '.join(required_cols)}")
        return

    st.write(df.keys())
    # Sum the columns to get total scores
    total_scores = {
        "md5": df["md5"].sum(),
        "sha256": df["sha256"].sum(),
        "xxh64sum": df["xxh64sum"].sum(),
        "b2sum": df["b2sum"].sum()
    }

    # Root score (can be total of all or left as 0 to hide the central wedge value)
    total_root_score = sum(total_scores.values())

    # Build the sunburst structure
    sunburst_df = pd.DataFrame({
        "parent": ["score"] * 4 + [""],
        "label": ["md5", "sha256", "xxh64sum", "b2sum", "score"],
        "value": [
            total_scores["md5"],
            total_scores["sha256"],
            total_scores["xxh64sum"],
            total_scores["b2sum"],
            0  # root node — value not used for sunburst
        ]
    })

    # Create the sunburst chart
    fig = px.sunburst(
        sunburst_df,
        names="label",
        parents="parent",
        values="value",
        title="Checksum Score Breakdown by Hash Algorithm"
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_mimetype_histogram(df: pd.DataFrame):
    """
    Plot a pie chart of file types by frequency.

    Parameters:
    - df (pd.DataFrame): DataFrame containing a 'filetype' column
    """
    if 'filetype' not in df.columns:
        st.warning("No 'mime-type' column found in the dataset.")
        return

    counts = (
        df["mime-type"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    counts.columns = ["mime-type", "count"]

    fig = px.pie(
        counts,
        names="mime-type",
        values="count",
        title="Mime-types Distribution",
        hole=0.3
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_filetype_histogram(df: pd.DataFrame):
    """
    Plot a pie chart of file types by frequency.

    Parameters:
    - df (pd.DataFrame): DataFrame containing a 'filetype' column
    """
    if 'filetype' not in df.columns:
        st.warning("No 'filetype' column found in the dataset.")
        return

    counts = (
        df["filetype"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    counts.columns = ["filetype", "count"]

    fig = px.pie(
        counts,
        names="filetype",
        values="count",
        title="File Types Distribution",
        hole=0.3
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_extension_histogram(df: pd.DataFrame):
    """
    Plot a bar chart of file extensions in ascending order of frequency.

    Parameters:
    - df (pd.DataFrame): DataFrame containing an 'extension' column
    """
    if 'extension' not in df.columns:
        st.warning("No 'extension' column found in the dataset.")
        return

    # Drop missing values and count extensions
    counts = (
        df["extension"]
        .dropna()
        .value_counts()
        .sort_values(ascending=True)
        .reset_index()
    )
    counts.columns = ["extension", "count"]

    # Create bar chart
    fig = px.bar(
        counts,
        x="extension",
        y="count",
        title="File Extension Histogram",
        labels={"extension": "File Extension", "count": "Frequency"},
        text="count",
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)

    # Display chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# ────────────────────────────────
# App Title and Introduction
# ────────────────────────────────
print_intro()

try:
    # ────────────────────────────────
    # Load and Parse JSON Data
    # ────────────────────────────────
    df = load_collection_data()

    # ────────────────────────────────
    # Collection Selection in Sidebar
    # ────────────────────────────────
    st.sidebar.header("📁 Collections")
    unique_collections = sorted(df["collection"].dropna().unique())
    default_index = unique_collections.index("26") if "26" in unique_collections else 0
    selected_collection = st.sidebar.selectbox(
        "Select a Collection", unique_collections, index=default_index
    )

    # Filter to selected collection
    collection_subset = df[df["collection"] == selected_collection]

    # ────────────────────────────────
    # BILD ID Selection in Sidebar
    # ────────────────────────────────
    st.sidebar.markdown("### 📌 Datasets in Collection")
    matching_bildids = sorted(collection_subset["bildid"].dropna().unique())
    selected_bildid = st.sidebar.selectbox("Select a Dataset (BILD ID)", matching_bildids)

    # Load selected dataset metadata
    data = load_dataset_data(selected_bildid)

    # Display metadata
    st.subheader("🧬 Dataset Metadata")
    st.write(f"**Metadata version:** {data.get('version', 'N/A')}")
    st.write(f"**General modality:** {data.get('modality', 'N/A')}")
    st.write(f"**Technique:** {data.get('technique', 'N/A')}")

    # ────────────────────────────────
    # Manifest Table and Plot
    # ────────────────────────────────
    if "manifest" in data:
        manifest_df = pd.DataFrame(data["manifest"])
        st.subheader("📄 Manifest Table")
        st.dataframe(manifest_df)

        st.subheader("📊 Checksums coverage report")
        plot_checksum_sunburst_from_df(manifest_df)

        st.subheader("📊 Useful Plots")
        plot_extension_histogram(manifest_df)
        plot_filetype_histogram(manifest_df)
        plot_mimetype_histogram(manifest_df)
        
    else:
        st.warning("⚠️ The 'manifest' key was not found in the dataset JSON.")

except Exception as e:
    st.error(f"❌ Failed to load or process data. More than likely inventory file has not been found.")
