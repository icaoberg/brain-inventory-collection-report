import streamlit as st
import plotly.express as px


def plot(df, selected_collection):
    # Filter to only datasets in selected collection
    bar_df = df[df["collection"] == selected_collection][
        ["collection", "bildid"]
    ].copy()

    # Sort rows by bildid (ascending)
    bar_df = bar_df.sort_values(by="bildid", ascending=True)

    # Add count column (each dataset = 1)
    bar_df["count"] = 1

    # Create bar chart (one bar per dataset)
    fig_bar = px.bar(
        bar_df,
        x="bildid",
        y="count",
        text="bildid",
        hover_data={"bildid": True, "count": False},
        title="Number of Datasets (One Bar per Dataset)",
        labels={"count": "Dataset", "bildid": "Brain ID"},
    )

    # Customize appearance
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(
        showlegend=False,
        xaxis=dict(tickangle=45),
        yaxis=dict(gridcolor="lightgray"),
    )

    st.plotly_chart(fig_bar, use_container_width=True)
