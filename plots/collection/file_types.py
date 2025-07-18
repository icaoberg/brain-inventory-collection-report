    st.subheader("🗂️ File Types Distribution")
    if "file_types" in df.columns and df["file_types"].notna().sum() > 0:
        filetype_counts = df["file_types"].dropna().value_counts()
        fig4, ax4 = plt.subplots(figsize=(6, 6))
        wedges, _, _ = ax4.pie(
            filetype_counts, labels=None, autopct="%1.1f%%", startangle=140
        )
        ax4.axis("equal")
        ax4.set_title("File Type Breakdown")
        ax4.legend(
            wedges,
            filetype_counts.index,
            title="File Types",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize="small",
        )
        st.pyplot(fig4)
    else:
        st.info("No file-type information is present.")