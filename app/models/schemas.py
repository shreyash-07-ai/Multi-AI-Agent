from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    document_ids: List[str] = Field(default_factory=list)
    generate_docx: bool = True
    generate_pptx: bool = True
    template_docx_id: Optional[str] = None
    template_pptx_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    version: int
    trace: List[str]
    sources: List[Dict[str, Any]]
    validation: Dict[str, Any]
    artifacts: Dict[str, str]
