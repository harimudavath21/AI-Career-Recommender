"""Resume text extraction helpers for PDF, DOCX and TXT files.

These functions are standalone and do not change the existing Streamlit app.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any
from io import BytesIO


def _read_bytes(source: Any) -> bytes:
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    if hasattr(source, "getvalue"):
        return source.getvalue()
    if hasattr(source, "read"):
        data = source.read()
        try:
            source.seek(0)
        except Exception:
            pass
        return data
    if isinstance(source, (str, Path)):
        return Path(source).read_bytes()
    raise TypeError("source must be a file path, bytes, or file-like object")


def extract_text(source: Any, filename: str | None = None) -> str:
    """Extract text from a PDF, DOCX or TXT path/bytes/uploaded file.

    Raises ValueError for unsupported formats and RuntimeError if an optional
    parser dependency is missing.
    """
    inferred_name = filename or getattr(source, "name", None) or (str(source) if isinstance(source, (str, Path)) else "")
    suffix = Path(inferred_name).suffix.lower()
    data = _read_bytes(source)
    if suffix == ".pdf":
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError("Install PyMuPDF to read PDF resumes: pip install pymupdf") from exc
        with fitz.open(stream=data, filetype="pdf") as pdf:
            return "\n".join(page.get_text("text") for page in pdf).strip()
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise RuntimeError("Install python-docx to read DOCX resumes: pip install python-docx") from exc
        document = Document(BytesIO(data))
        chunks = [p.text for p in document.paragraphs if p.text.strip()]
        for table in document.tables:
            for row in table.rows:
                chunks.append(" | ".join(cell.text.strip() for cell in row.cells))
        return "\n".join(chunks).strip()
    if suffix in {".txt", ".text"}:
        return data.decode("utf-8-sig", errors="replace").strip()
    raise ValueError(f"Unsupported resume format: {suffix or 'unknown'}. Use PDF, DOCX or TXT.")


def extract_resume_text(source: Any, filename: str | None = None) -> str:
    """Alias retained for callers that prefer an explicit function name."""
    return extract_text(source, filename)
