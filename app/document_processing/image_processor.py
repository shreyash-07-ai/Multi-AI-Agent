from .ocr_processor import extract_image_text

def analyze_image(path):
    return {"type": "image", "text": extract_image_text(path)}
