import plotly.express as px
import streamlit as st
import pandas as pd

def plot(df, selected_collection):
    collection_subset = df[df["collection"] == selected_collection]

    if (
        "contributor" in collection_subset.columns
        and "affiliation" in collection_subset.columns
        and collection_subset["contributor"].notna().sum() > 0
        and collection_subset["affiliation"].notna().sum() > 0
    ):
        # Count (affiliation, contributor) pairs
        counts = (
            collection_subset
            .groupby(["affiliation", "contributor"])
            .size()
            .reset_index(name="count")
        )

        # Create treemap
        fig = px.treemap(
            counts,
            path=["affiliation", "contributor"],
            values="count",
            title="Contributors by Affiliation in Selected Collection"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No contributor or affiliation information is present for the selected collection.")
