import os
import platform
import shutil
import subprocess
from typing import Tuple, Optional


def _detect_ghostscript() -> Tuple[Optional[str], Optional[str]]:
    """
    Detect Ghostscript executable in a cross-platform way.
    Returns (exe_name_or_path, hint_message_if_missing).
    """
    system = platform.system().lower()

    if system == "windows":
        # Try 64-bit then 32-bit names
        for exe in ("gswin64c", "gswin32c"):
            path = shutil.which(exe)
            if path:
                return path, None
        return None, (
            "Ghostscript not found. Install it from ghostscript.com and "
            "add its bin folder to PATH (e.g., C:\\Program Files\\gs\\gs10.x\\bin)."
        )

    # macOS/Linux typically expose 'gs'
    path = shutil.which("gs")
    if path:
        return path, None
    return None, (
        "Ghostscript ('gs') not found. Install it via your package manager "
        "(e.g., brew install ghostscript on macOS, apt-get install ghostscript on Linux)."
    )


def compress_pdf(input_path: str, output_path: str, profile: str, dpi: int=100) -> dict:
    """
    Compress a PDF using Ghostscript.
    Returns a dict: {'ok': bool, 'size_mb': float, 'error': Optional[str]}
    """
    # Map human labels to Ghostscript quality profiles
    profile_map = {
        "Max Compression (/screen)": "/screen",
        "Balanced (/ebook)": "/ebook",
        "High Quality (/printer)": "/printer",
    }
    gs_profile = profile_map.get(profile, "/ebook")

    # Detect Ghostscript
    gs_path, hint = _detect_ghostscript()
    if not gs_path:
        return {"ok": False, "size_mb": float("inf"), "error": hint}

    # Ensure parent folders exist for output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Build Ghostscript command
    # -dNOPAUSE/-dBATCH/-dQUIET for non-interactive execution
    command = [
        gs_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={gs_profile}",
        "-dDownsampleColorImages=true",
        "-dDownsampleGrayImages=true",
        "-dDownsampleMonoImages=true",
        f"-dColorImageResolution={dpi}",
        f"-dGrayImageResolution={dpi}",
        f"-dMonoImageResolution={dpi}",
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        "-o", output_path,
        input_path,
    ]

    try:
        # Run Ghostscript and check for non-zero exit status
        subprocess.run(command, check=True)
        if not os.path.exists(output_path):
            return {
                "ok": False,
                "size_mb": float("inf"),
                "error": "Output file was not created. Check input validity and permissions."
            }
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        return {"ok": True, "size_mb": size_mb, "error": None}
    except subprocess.CalledProcessError as e:
        return {
            "ok": False,
            "size_mb": float("inf"),
            "error": f"Ghostscript failed (exit code {e.returncode})."
        }
    except Exception as e:
        return {"ok": False, "size_mb": float("inf"), "error": f"Compression error: {e}"}
