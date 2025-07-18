import streamlit as st
from datetime import datetime

def print_intro():
    st.title("🧠 Brain Image Library Inventory Report")

    st.markdown(
        """
        The **Brain Image Library (BIL)** is a national public resource that supports the storage, sharing, and analysis of large-scale brain imaging datasets. 
        This report provides a snapshot of the current dataset inventory, highlighting key metadata including file counts, sizes, and organizational structure.
        """
    )

    # Display today's date
    today_str = datetime.today().strftime("%B %d, %Y")
    st.markdown(f"### 📅 Report Date: {today_str}")