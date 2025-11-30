import os
import subprocess
import platform
import shutil
from dotenv import load_dotenv

load_dotenv()

def _detect_ghostscript() -> str:
    # Priority: .env override
    override = os.getenv("GHOSTSCRIPT_PATH")
    if override and shutil.which(override):
        return override

    # Auto-detect based on platform
    system = platform.system().lower()
    candidates = []

    if system == "windows":
        candidates = ["gswin64c", "gswin32c"]
    else:
        candidates = ["gs"]

    for exe in candidates:
        path = shutil.which(exe)
        if path:
            return path

    raise FileNotFoundError("Ghostscript executable not found. Set GHOSTSCRIPT_PATH in .env or add to PATH.")

def compress_pdf(input_path, output_path, profile, dpi=100):
    profile_map = {
        "Max Compression (/screen)": "/screen",
        "Balanced (/ebook)": "/ebook",
        "High Quality (/printer)": "/printer"
    }
    gs_profile = profile_map.get(profile, "/ebook")

    try:
        gs_path = _detect_ghostscript()
        command = [
            gs_path,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={gs_profile}",
            "-dDownsampleColorImages=true",
            f"-dColorImageResolution={dpi}",
            "-o", output_path,
            input_path
        ]
        subprocess.run(command, check=True)
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        return {"ok": True, "size_mb": size_mb, "error": None}
    except Exception as e:
        return {"ok": False, "size_mb": float("inf"), "error": str(e)}
