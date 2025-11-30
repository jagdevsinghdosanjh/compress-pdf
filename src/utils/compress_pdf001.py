import os
import subprocess
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

def compress_pdf(input_path: str, output_path: str, profile: str, dpi: int = 100) -> dict:
    profile_map = {
        "Max Compression (/screen)": "/screen",
        "Balanced (/ebook)": "/ebook",
        "High Quality (/printer)": "/printer",
    }
    gs_profile = profile_map.get(profile, "/ebook")

    # Get Ghostscript path from .env or fallback to system PATH
    gs_path = os.getenv("GHOSTSCRIPT_PATH", "gs")

    command = [
        gs_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={gs_profile}",
        "-dDownsampleColorImages=true",
        f"-dColorImageResolution={dpi}",
        "-o", output_path,
        input_path,
    ]

    try:
        subprocess.run(command, check=True)
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        return {"ok": True, "size_mb": size_mb, "error": None}
    except Exception as e:
        return {"ok": False, "size_mb": float("inf"), "error": str(e)}
