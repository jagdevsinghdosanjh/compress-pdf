import os
import fitz  # PyMuPDF

def compress_pdf(input_path: str, output_path: str, zoom: float = 0.5) -> dict:
    """
    Compress a PDF using PyMuPDF by rasterizing pages at a lower zoom.
    Args:
        input_path: Path to input PDF
        output_path: Path to save compressed PDF
        zoom: Scale factor (0.5 = 50% size, smaller = more compression)

    Returns:
        dict: {'ok': bool, 'size_mb': float, 'error': Optional[str]}
    """
    try:
        doc = fitz.open(input_path)
        new_doc = fitz.open()

        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img_pdf = fitz.open(stream=pix.tobytes("png"), filetype="png")
            new_doc.insert_pdf(img_pdf)

        new_doc.save(output_path, deflate=True)
        doc.close()
        new_doc.close()

        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        return {"ok": True, "size_mb": size_mb, "error": None}

    except Exception as e:
        return {"ok": False, "size_mb": float("inf"), "error": str(e)}
