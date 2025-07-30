# 🧠 Brain Image Library Observational Dashboard

This Streamlit application provides an interactive dashboard for exploring publicly available metadata from the [Brain Image Library (BIL)](https://www.brainimagelibrary.org/). The app enables users to select collections and datasets, view detailed metadata, and visualize key attributes such as file types, MIME types, and checksums.

---

## 🚀 Features

- 📁 Browse and filter BIL dataset collections
- 📄 View and inspect individual dataset metadata
- 📊 Visualize file extensions, MIME types, and file types with interactive charts
- 🧮 Compute dataset statistics (e.g., mean checksum scores, total size)
- ✅ Highlight datasets with tracings or key metadata present
- 🔍 Built with public metadata from BIL (no sensitive data used)

---

# 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt\
```

then run the app

```bash
streamlit run app.py
```

## 📝 Disclaimer
This application is an observational tool built using publicly available metadata from the Brain Image Library (BIL). It is intended solely for exploratory and visualization purposes. The app does not host, modify, or redistribute any original imaging data from BIL. All dataset rights and acknowledgments remain with their original contributors.

Please note that the information presented here reflects metadata made publicly available through BIL services and is not guaranteed to be comprehensive or current.

