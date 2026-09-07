from PIL import Image

def extract_image_text(path):
    try:
        import pytesseract
        return pytesseract.image_to_string(Image.open(path)).strip()
    except Exception as e:
        return f"[OCR unavailable: {e}]"
