from pathlib import Path
from uuid import uuid4

from app.agents.supervisor_agent import SupervisorAgent
from app.agents.validation_agent import validate
from app.generation.docx_generator import generate_docx
from app.generation.pptx_generator import generate_pptx
from app.rag.ingestion import ingest_file
from app.versioning.version_manager import save_version
from app.config import OUTPUT_DIR, UPLOAD_DIR


def upload_file(file_name: str, file_bytes: bytes):
    """Save and index an uploaded file without requiring FastAPI."""
    allowed = {".pdf", ".docx", ".pptx", ".png", ".jpg", ".jpeg", ".webp"}
    ext = Path(file_name or "").suffix.lower()
    if ext not in allowed:
        raise ValueError("Unsupported file type")

    file_id = uuid4().hex
    path = UPLOAD_DIR / f"{file_id}{ext}"
    path.write_bytes(file_bytes)

    try:
        chunks = ingest_file(str(path), file_id)
    except Exception:
        path.unlink(missing_ok=True)
        raise

    return {
        "file_id": file_id,
        "filename": file_name,
        "path": str(path),
        "chunks": chunks,
    }


def run_workflow(
    message: str,
    document_paths: list[str],
    session_id: str,
    generate_docx_file: bool = True,
    generate_pptx_file: bool = True,
):
    """Run the same agent/generation pipeline used by the FastAPI endpoint."""
    result = SupervisorAgent().run(message, document_paths)
    content = result["content"]

    artifacts = {}

    if generate_docx_file:
        path = OUTPUT_DIR / f"{session_id}_v1.docx"
        generate_docx(content, path, None)
        artifacts["docx"] = str(path)

    if generate_pptx_file:
        path = OUTPUT_DIR / f"{session_id}_v1.pptx"
        generate_pptx(content, path, None, target_slides=12)
        artifacts["pptx"] = str(path)

    validation = validate(artifacts)
    version = save_version(session_id, artifacts, result["trace"])

    return {
        "answer": content.get("executive_summary", "Artifacts generated."),
        "version": version,
        "trace": result["trace"],
        "sources": result["web"],
        "validation": validation,
        "artifacts": artifacts,
    }
