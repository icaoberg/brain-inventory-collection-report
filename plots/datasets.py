def plot_extension_histogram(df: pd.DataFrame):
    """
    Creates and displays a histogram of the 'extension' column in the DataFrame using Streamlit and Plotly.

    Args:
        df (pd.DataFrame): The DataFrame containing a column named 'extension'.
    """
    if "extension" not in df.columns:
        st.error("The DataFrame must contain a column named 'extension'.")
        return

    # Count occurrences
    extension_counts = df["extension"].dropna().value_counts().reset_index()
    extension_counts.columns = ["extension", "count"]
    extension_counts.sort_values(by="count", inplace=True)

    # Create histogram
    fig = px.bar(
        extension_counts,
        x="extension",
        y="count",
        title="Histogram of File Extensions",
        labels={"extension": "File Extension", "count": "Frequency"},
    )
    fig.update_layout(xaxis_tickangle=-45)

    # Display chart
    st.plotly_chart(fig, use_container_width=True)