from pathlib import Path
from .pdf_processor import extract_pdf
from .docx_processor import analyze_docx
from .pptx_processor import analyze_pptx
from .image_processor import analyze_image

def analyze_file(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return {"type": "pdf", "pages": extract_pdf(path)}
    if ext == ".docx":
        return analyze_docx(path)
    if ext == ".pptx":
        return analyze_pptx(path)
    if ext in {".png", ".jpg", ".jpeg", ".webp"}:
        return analyze_image(path)
    raise ValueError(f"Unsupported file type: {ext}")

def extract_text(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return "\n".join(x["text"] for x in extract_pdf(path))
    if ext == ".docx":
        from .docx_processor import extract_text as f
        return f(path)
    if ext == ".pptx":
        from .pptx_processor import extract_text as f
        return f(path)
    if ext in {".png", ".jpg", ".jpeg", ".webp"}:
        return analyze_image(path)["text"]
    raise ValueError(f"Unsupported file type: {ext}")
