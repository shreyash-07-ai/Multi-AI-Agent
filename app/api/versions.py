from fastapi import APIRouter
from app.versioning.version_manager import get_versions
router = APIRouter()

@router.get("/versions/{session_id}")
def versions(session_id: str):
    return get_versions(session_id)
