import streamlit as st
import pandas as pd

from plots.download_and_get_data import load_collection_data, load_dataset_data
from plots.intro import print_dataset_intro as print_intro
import plotly.express as px

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
        title="File Extension Histogram (Ascending Order)",
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

        st.subheader("📊 Extension Histogram")
        plot_extension_histogram(df)
    else:
        st.warning("⚠️ The 'manifest' key was not found in the dataset JSON.")

except Exception as e:
    st.error(f"❌ Failed to load or process data: {e}")
