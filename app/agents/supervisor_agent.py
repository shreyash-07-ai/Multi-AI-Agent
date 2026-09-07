from pathlib import Path
from .rag_agent import run_rag
from .web_research_agent import research
from .generation_agent import create_content
from .document_analysis_agent import analyze as analyze_document
from .ppt_analysis_agent import analyze as analyze_ppt
from app.config import UPLOAD_DIR

class SupervisorAgent:
    def run(self, query, file_paths):
        trace = ["Supervisor: request received and workflow selected"]
        rag = run_rag(query)
        trace.append(f"RAG Agent: retrieved {sum(1 for x in rag if x.get('text'))} relevant chunks")

        web = []
        needs_web = any(k in query.lower() for k in [
            "latest", "current", "research", "trend", "market", "recent", "web"
        ])
        if needs_web:
            try:
                web = research(query)
                trace.append(f"Web Research Agent: collected {len(web)} sources")
            except Exception as e:
                trace.append(f"Web Research Agent: unavailable ({e})")

        doc_analysis = None
        ppt_analysis = None
        for p in file_paths:
            ext = Path(p).suffix.lower()
            if ext == ".docx":
                try:
                    doc_analysis = analyze_document(p)
                    trace.append("Document Analysis Agent: analyzed DOCX structure/style")
                except Exception as e:
                    trace.append(f"Document Analysis Agent: {e}")
            elif ext == ".pptx":
                try:
                    ppt_analysis = analyze_ppt(p)
                    trace.append("PPT Analysis Agent: analyzed slide layouts/style")
                except Exception as e:
                    trace.append(f"PPT Analysis Agent: {e}")

        content = create_content(query, rag, web, doc_analysis, ppt_analysis)
        trace.append("Content Planning Agent: created structured content")
        return {"rag": rag, "web": web, "content": content, "trace": trace}
