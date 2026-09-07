from fastapi import APIRouter
from app.config import OUTPUT_DIR
router = APIRouter()

@router.get("/artifacts")
def artifacts():
    return [{"name": p.name, "path": str(p), "size": p.stat().st_size} for p in OUTPUT_DIR.iterdir() if p.is_file()]
