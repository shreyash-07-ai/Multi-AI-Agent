from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import UPLOAD_DIR
from app.rag.ingestion import ingest_file

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    allowed = {".pdf", ".docx", ".pptx", ".png", ".jpg", ".jpeg", ".webp"}
    ext = Path(file.filename or "").suffix.lower()
    if ext not in allowed:
        raise HTTPException(400, "Unsupported file type")
    file_id = uuid4().hex
    path = UPLOAD_DIR / f"{file_id}{ext}"
    path.write_bytes(await file.read())
    try:
        chunks = ingest_file(str(path), file_id)
    except Exception as e:
        raise HTTPException(500, f"Upload succeeded but indexing failed: {e}")
    return {"file_id": file_id, "filename": file.filename, "path": str(path), "chunks": chunks}
