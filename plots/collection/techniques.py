import plotly.express as px
import streamlit as st
import pandas as pd

def plot(df, selected_collection):
    collection_subset = df[df["collection"] == selected_collection]

    if (
        "technique" in collection_subset.columns
        and "generalmodality" in collection_subset.columns
        and collection_subset["technique"].notna().sum() > 0
        and collection_subset["generalmodality"].notna().sum() > 0
    ):
        # Group and count by generalmodality and technique
        counts = (
            collection_subset
            .groupby(["generalmodality", "technique"])
            .size()
            .reset_index(name="count")
        )

        # Create treemap
        fig = px.treemap(
            counts,
            path=["generalmodality", "technique"],
            values="count",
            title="Techniques by General Modality in Selected Collection"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No technique or generalmodality information is present for the selected collection.")
