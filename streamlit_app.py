    # Pie Chart of all datasets in selected collection
    st.subheader("📈 File Distribution in Selected Collection")

    pie_data = df[df["collection"] == selected_collection].set_index("bildid")["number_of_files"]
    pie_data = pie_data[pie_data > 0].sort_values(ascending=False)

    fig3, ax3 = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax3.pie(
        pie_data,
        labels=None,
        autopct="%1.1f%%",
        startangle=140
    )
    ax3.axis("equal")
    ax3.set_title("Number of Files per Dataset")

    # Format legend into columns of 25 items
    labels = list(pie_data.index)
    num_cols = (len(labels) - 1) // 25 + 1

    ax3.legend(
        wedges,
        labels,
        title="Brain ID",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize="small",
        ncol=num_cols
    )

    st.pyplot(fig3)
