    st.subheader("📄 MIME Types Distribution")
    if "mime_types" in df.columns and df["mime_types"].notna().sum() > 0:
        mime_counts = df["mime_types"].dropna().value_counts()
        fig5, ax5 = plt.subplots(figsize=(6, 6))
        wedges, _, _ = ax5.pie(
            mime_counts, labels=None, autopct="%1.1f%%", startangle=140
        )
        ax5.axis("equal")
        ax5.set_title("MIME Type Breakdown")
        ax5.legend(
            wedges,
            mime_counts.index,
            title="MIME Types",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize="small",
        )
        st.pyplot(fig5)
    else:
        st.info("No MIME-type information is present.")