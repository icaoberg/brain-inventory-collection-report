import streamlit as st
import plotly.express as px


def plot(df, selected_collection):
    st.subheader("🏛️ Dataset Distribution by Contributors")
    collection_subset = df[df["collection"] == selected_collection]

    if (
        "contributors" in collection_subset.columns
        and collection_subset["contributor"].notna().sum() > 0
    ):
        counts = collection_subset["contributors"].dropna().value_counts()
        fig = px.pie(
            names=counts.index,
            values=counts.values,
            title="Contributors in Selected Collection",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No contributor information is present for the selected collection.")
