from streamlit_image_gallery import streamlit_image_gallery
import streamlit as st
import pandas as pd
import humanize
from plots.download_and_get_data import load_collection_data, load_dataset_data
from plots.intro import print_dataset_intro as print_intro
import plotly.express as px
import brainimagelibrary as brainzzz
import json

def get_brainpi_link(download_url: str) -> str | None:
    """
    Convert a BIL download URL to a BrainAPI OSD URL if it's a .tif or .jp2 file.
    
    Args:
        download_url (str): The original download URL.
    
    Returns:
        str | None: The transformed URL or None if not a supported image format.
    """
    if download_url.endswith(('.tif', '.jp2')):
        return download_url.replace(
            'https://download.brainimagelibrary.org/',
            'https://brainapi.brainimagelibrary.org/osd/bil_data/'
        )
    return None


def plot_mimetype_histogram(df: pd.DataFrame):
    """
    Plot a bar chart of MIME types by frequency.

    Parameters:
    - df (pd.DataFrame): DataFrame containing a 'mime-type' column
    """
    if 'mime-type' not in df.columns:
        st.warning("No 'mime-type' column found in the dataset.")
        return

    counts = (
        df["mime-type"]
        .dropna()
        .value_counts()
        .sort_values(ascending=True)
        .reset_index()
    )
    counts.columns = ["mime-type", "count"]

    fig = px.bar(
        counts,
        x="mime-type",
        y="count",
        title="MIME Type Frequency",
        labels={"mime-type": "MIME Type", "count": "Count"},
        text="count"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=False)

def plot_filetype_histogram(df: pd.DataFrame):
    """
    Plot a bar chart of file types by frequency.

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
        .sort_values(ascending=True)
        .reset_index()
    )
    counts.columns = ["filetype", "count"]

    fig = px.bar(
        counts,
        x="filetype",
        y="count",
        title="File Type Frequency",
        labels={"filetype": "File Type", "count": "Count"},
        text="count"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=False)


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
    st.plotly_chart(fig, use_container_width=False)

# ────────────────────────────────
# App Title and Introduction
# ────────────────────────────────
st.set_page_config(layout="wide")
print_intro()

try:
    # ────────────────────────────────
    # Load and Parse JSON Data
    # ────────────────────────────────
    df = load_collection_data()

    # ────────────────────────────────
    # Collection Selection in Sidebar
    # ────────────────────────────────
    st.sidebar.header("📁 Submissions")
    unique_collections = sorted(df["collection"].dropna().unique())
    default_index = unique_collections.index("0500368854") if "0500368854" in unique_collections else 0
    selected_collection = st.sidebar.selectbox(
        "Select Submission", unique_collections, index=default_index
    )

    # Filter to selected collection
    collection_subset = df[df["collection"] == selected_collection]

    # ────────────────────────────────
    # BILD ID Selection in Sidebar
    # ────────────────────────────────
    st.sidebar.markdown("### 📌 Datasets in Submission")
    matching_bildids = sorted(collection_subset["bildid"].dropna().unique())
    selected_bildid = st.sidebar.selectbox("Select a Dataset (BILD ID)", matching_bildids)

    # Load selected dataset metadata
    data = load_dataset_data(selected_bildid)

    # ────────────────────────────────
    # Manifest Table and Plot
    # ────────────────────────────────
    if "manifest" in data:
        manifest_df = pd.DataFrame(data["manifest"])
        manifest_df['brainpi_url'] = manifest_df['download_url'].apply(get_brainpi_link)

        # Check if any 'filetype' contains the word 'tracing' (case-insensitive)
        has_tracing = manifest_df["filetype"].dropna().str.contains("tracing", case=False).any()
        has_matrices = manifest_df["filename"].dropna().str.contains("cell_by_gene.h5ad", case=False).any()

        # Display metadata
        st.subheader("🧬 Dataset Summary")
        st.markdown(
            f"""
        - **Status:** {data.get('status', 'N/A')}
        - **Metadata version:** {data.get('version', 'N/A')}
        - **General modality:** {data.get('modality', 'N/A')}
        - **Technique:** {data.get('technique', 'N/A')}
        - **Species:** {data.get('species', 'N/A')}
        - **Location:** {data.get('directory', 'N/A')}
        - **Number of files:** {len(manifest_df)}
        - **Dataset size:** {humanize.naturalsize(manifest_df['size'].dropna().sum(), binary=True)}
        - **Has DOI:** {"✅" if brainzzz.dois.__get_datacite_metadata(dataset_id=selected_bildid) else "❌"}
        - **Has tracings:** {"✅" if has_tracing else "❌"}
        - **Has cell by genes matrices:** {"✅" if has_tracing else "❌"}
        """
        )

        if not manifest_df['brainpi_url'].dropna().eq('').all():
            st.subheader("🧠 Viz")
            # Filter out empty or null URLs
            valid_df = manifest_df[manifest_df['brainpi_url'].notna() & (manifest_df['brainpi_url'] != '')]

            # Build gallery input: each item has 'src' and 'title'
            images = [
                {
                    "src": url,
                    "title": str(row['filename']) if 'filename' in manifest_df.columns else url
                }
                for _, row in valid_df.iterrows()
                for url in [row['brainpi_url']]
            ]

            # Display gallery if there are images
            if images:
                st.subheader("🧠 Viz Gallery")
                streamlit_image_gallery(images=images, height=300)
            else:
                st.info("No BrainPI visualizations available.")

        with st.expander("🧬 Checksum coverage"):
            checksums = {'md5', 'sha256', 'xxh64', 'b2sum'}
            for checksum in checksums:
                if checksum in manifest_df.keys():
                    score = manifest_df[checksum].notna().notnull().mean()
                else:
                    score = 0
                st.markdown(f"- **{checksum.upper()}:** {score}\%")

        with st.expander("📄 Manifest Table"):
            st.dataframe(
                manifest_df[["filename", "filetype", "download_url"]]
                .rename(columns={
                    "filename": "File Name",
                    "filetype": "Type",
                    "download_url": "Download URL"
                })
            )

        with st.expander("📄 Datacite"):
            try:
                st.json(json.loads(brainzzz.dois.__get_datacite_metadata(dataset_id=selected_bildid)))
            except:
                st.error(f"❌ Failed to load or process data from Datacite.")

        with st.expander("📊 Useful Plots"):
            plot_extension_histogram(manifest_df)
            plot_filetype_histogram(manifest_df)
            #plot_mimetype_histogram(manifest_df)
    else:
        st.warning("⚠️ The 'manifest' key was not found in the dataset JSON.")

except Exception as e:
    st.error(f"❌ Failed to load or process data. More than likely inventory file has not been found.")

with st.expander("ℹ️ Copyright and Funding Disclosure"):
    st.markdown(
        """
        This application is an observational tool built using publicly available metadata from the Brain Image Library (BIL). It is intended solely for exploratory and visualization purposes. The app does not host, modify, or redistribute any original imaging data from BIL. All dataset rights and acknowledgments remain with their original contributors.
        Please note that the information presented here reflects metadata made publicly available through BIL services and is not guaranteed to be comprehensive or current.

        The Brain Image Library is supported by the National Institutes of Mental Health of the National Institutes of Health under award number **R24-MH-114793**.  
        The content is solely the responsibility of the authors and does not necessarily represent the official views of the National Institutes of Health.  
        """
    )

