import streamlit as st
import plotly.express as px

def plot(df, selected_collection):
    collection_subset = df[df["collection"] == selected_collection]

    if (
        "generalmodality" in collection_subset.columns
        and collection_subset["generalmodality"].notna().sum() > 0
    ):
        counts = collection_subset["generalmodality"].dropna().value_counts()
        fig = px.pie(
            names=counts.index,
            values=counts.values,
            title="Modalities in Selected Collection",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No modality information is present for the selected collection.")
