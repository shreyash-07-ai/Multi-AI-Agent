import fitz

def extract_pdf(path):
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text").strip()
        pages.append({"page": i + 1, "text": text})
    return pages

def extract_text(path):
    return "\n".join(p["text"] for p in extract_pdf(path))
