from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest
from app.agents.supervisor_agent import SupervisorAgent
from app.generation.docx_generator import generate_docx
from app.generation.pptx_generator import generate_pptx
from app.agents.validation_agent import validate
from app.versioning.version_manager import save_version
from app.config import UPLOAD_DIR, OUTPUT_DIR

router = APIRouter()

@router.post("/chat")
def chat(req: ChatRequest):
    paths = []
    for file_id in req.document_ids:
        matches = list(UPLOAD_DIR.glob(f"{file_id}.*"))
        if matches:
            paths.append(str(matches[0]))

    try:
        result = SupervisorAgent().run(req.message, paths)
    except Exception as e:
        raise HTTPException(500, str(e))

    artifacts = {}
    content = result["content"]

    doc_template = None
    ppt_template = None
    if req.template_docx_id:
        m = list(UPLOAD_DIR.glob(f"{req.template_docx_id}.docx"))
        doc_template = str(m[0]) if m else None
    if req.template_pptx_id:
        m = list(UPLOAD_DIR.glob(f"{req.template_pptx_id}.pptx"))
        ppt_template = str(m[0]) if m else None

    if req.generate_docx:
        path = OUTPUT_DIR / f"{req.session_id}_v1.docx"
        generate_docx(content, path, doc_template)
        artifacts["docx"] = str(path)

    if req.generate_pptx:
        path = OUTPUT_DIR / f"{req.session_id}_v1.pptx"
        generate_pptx(content, path, ppt_template, target_slides=12)
        artifacts["pptx"] = str(path)

    validation = validate(artifacts)
    version = save_version(req.session_id, artifacts, result["trace"])
    return {
        "answer": content.get("executive_summary", "Artifacts generated."),
        "version": version,
        "trace": result["trace"],
        "sources": result["web"],
        "validation": validation,
        "artifacts": artifacts,
    }
