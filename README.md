# Bulk PDF Compressor

A cross‑platform Streamlit app that compresses PDFs using Ghostscript.

## Setup
1. Create a virtual environment (optional) and activate it.
2. `pip install -r requirements.txt`
3. Install Ghostscript:
   - Windows: Install Ghostscript and ensure its `bin` folder is in PATH.
   - macOS: `brew install ghostscript`
   - Linux: `sudo apt-get install ghostscript`

## Run
```bash
streamlit run src/main.py

Notes
Profiles:

/screen: smallest size, lowest quality

/ebook: balanced

/printer: higher quality, larger size

Adjust DPI to trade off image quality vs. file size.

Outputs saved to data/compressed/.


---

## Troubleshooting and tips

- **Ghostscript not detected:**
  - **Windows:** Add Ghostscript’s bin folder to PATH. Example: `C:\Program Files\gs\gs10.x\bin`.
  - **macOS/Linux:** Make sure `gs` is available (`which gs`). Install via package manager.

- **Still getting large files:**
  - **Lower DPI:** Try 75 or 50.
  - **Use `/screen`:** Max compression.
  - **Remove high-res scans:** Some PDFs with embedded images won’t compress much due to inherent content.

- **File permissions:**
  - **Ensure write access:** The app writes to `data/` and `data/compressed/`.

---

## Optional enhancements

- **Add a badge overlay:** Show a 🎖️ when size < 2 MB.
- **Batch progress:** Use `st.progress` for multiple files.
- **Logs:** Save a CSV in `data/` with input size, output size, profile, DPI, and timestamp.

If you want, I’ll scaffold a badge utility and a simple compression log next.