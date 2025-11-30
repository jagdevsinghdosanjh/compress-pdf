import os
import streamlit as st
from utils import compress_pdf

st.set_page_config(page_title="Bulk PDF Compressor", layout="wide")
st.title("📄 Bulk PDF Compressor (<7 MB)")

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("data/compressed", exist_ok=True)

# UI controls
profile = st.selectbox(
    "Choose Compression Profile",
    options=["Max Compression (/screen)", "Balanced (/ebook)", "High Quality (/printer)"],
    index=0
)

dpi = st.slider("Image DPI (lower = smaller size)", min_value=10, max_value=300, value=100, step=25)

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.write("### Compression Results")
    for uploaded_file in uploaded_files:
        # Save input
        input_path = os.path.join("data", uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Compress
        output_name = f"compressed_{uploaded_file.name}"
        output_path = os.path.join("data/compressed", output_name)
        result = compress_pdf(input_path, output_path, profile, dpi)

        # Report
        if result["ok"] and result["size_mb"] < 7:
            st.success(f"{uploaded_file.name} → {result['size_mb']:.2f} MB ✅")
            with open(output_path, "rb") as f:
                st.download_button("Download Compressed PDF", f, file_name=output_name)
        elif result["ok"]:
            st.warning(f"{uploaded_file.name} is {result['size_mb']:.2f} MB ⚠️")
            with open(output_path, "rb") as f:
                st.download_button("Download Compressed PDF (above 7 MB)", f, file_name=output_name)
        else:
            st.error(f"{uploaded_file.name} failed: {result['error']}")
