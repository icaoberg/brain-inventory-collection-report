import streamlit as st
from datetime import datetime

def print_collection_intro():
    st.title("🧠 Brain Image Library Inventory Daily Report")

    st.markdown(
        """
        The **Brain Image Library (BIL)** is a national public resource that supports the storage, sharing, and analysis of large-scale brain imaging datasets. 
        This report provides a snapshot of the current dataset inventory, highlighting key metadata including file counts, sizes, and organizational structure.
        """
    )

    # Display today's date
    today_str = datetime.today().strftime("%B %d, %Y")
    st.markdown(f"### 📅 Report Date: {today_str}")

def print_dataset_intro():
    st.title("🧠 Brain Image Library Datasets")

    st.markdown(
        """
        The **Brain Image Library (BIL)** is a national public resource dedicated to the storage, sharing, and analysis of large-scale brain imaging datasets.  
        This report offers an overview of the diverse datasets within the BIL collection, which include multiple imaging modalities, species, and experimental techniques.  
        It highlights key metadata such as the number of files, total data volume, and organizational structure to help users understand the scope and composition of the archive.
        """
    )

    # Display today's date
    today_str = datetime.today().strftime("%B %d, %Y")
    st.markdown(f"📅 Report Date: {today_str}")