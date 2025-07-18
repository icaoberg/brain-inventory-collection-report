import streamlit as st
import plotly.express as px

def plot(df, selected_collection):
    st.subheader("🏛️ Dataset Distribution by Affiliation (Selected Collection)")
    collection_subset = df[df["collection"] == selected_collection]
    
    if "affiliation" in collection_subset.columns and collection_subset["affiliation"].notna().sum() > 0:
        counts = collection_subset["affiliation"].dropna().value_counts()
        fig = px.pie(
            names=counts.index,
            values=counts.values,
            title="Affiliations in Selected Collection"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No affiliation information is present for the selected collection.")