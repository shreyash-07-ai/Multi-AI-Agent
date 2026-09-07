# Multi-Agent AI Chatbot for Document & PPT Generation

A Docker-free enterprise POC implementing the assignment workflow:
- Supervisor/orchestrator
- DOCX/PDF/PPTX/image analysis
- OCR for scanned images
- real-time web research
- enterprise RAG with Gemini embeddings + Pinecone
- editable DOCX generation
- editable PPTX generation
- conversational editing foundation
- validation
- citations/traceability
- version management
- FastAPI backend + Streamlit UI
- Celery/Redis integration for background ingestion

## 1. Setup

Create the environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit only `.env` with your real API keys:

```env
GEMINI_API_KEY=...
PINECONE_API_KEY=...
PINECONE_INDEX=multi-agent-rag
```

The project can automatically create the Pinecone index if it does not exist. It uses 64-dimensional `text-embedding-3-small` embeddings.

## 2. Run

Terminal 1:
```powershell
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Terminal 2:
```powershell
.venv\Scripts\activate
streamlit run frontend/app.py
```

Celery/Redis are included for the assignment architecture. If Redis is installed locally, run:

```powershell
celery -A app.tasks.celery_app.celery worker --loglevel=INFO
```

The demo UI performs ingestion synchronously so the POC remains easy to run; the Celery task is available for asynchronous deployment.

## 3. Test

Open Streamlit and upload:
- `samples/Enterprise_Knowledge.pdf`
- `samples/Company_Proposal_Template.docx`
- `samples/Company_Presentation_Template.pptx`

Use:
> Research the latest Generative AI trends and create a proposal and a 12-slide presentation using the same tone and style as the uploaded files.

Then download the generated DOCX and PPTX.

## Assignment coverage

| Requirement | Implementation |
|---|---|
| Multi-agent orchestration | SupervisorAgent + specialized agents |
| Document analysis | PDF/DOCX/PPTX/image processors |
| PPT analysis | PPT Analysis Agent |
| Web research | DuckDuckGo HTML research |
| Enterprise RAG | Gemini embeddings + Pinecone |
| OCR | Tesseract integration |
| Editable DOCX | python-docx |
| Editable PPTX | python-pptx |
| Style/template preservation | Uses uploaded DOCX/PPTX styles/layouts as generation base |
| Conversational editing | Editing Agent foundation + versioned workflow |
| Citations | Web source list + generated source section |
| Validation | Artifact validation agent |
| Versioning | JSON version manager |
| Secure modular backend | FastAPI modules |
| Celery/Redis | Included task worker integration |
| Docker | Not required |


## Gemini setup

This version uses the Google Gemini API instead of OpenAI.

1. Copy `.env.example` to `.env`.
2. Put your Gemini API key in `GEMINI_API_KEY`.
3. Keep `PINECONE_API_KEY` if you want Pinecone-backed RAG.
4. The RAG embedding dimension is **768**, so this version uses a separate Pinecone index name: `multi-agent-rag-gemini`.

The project uses the current Google GenAI Python SDK (`google-genai`) with `models.generate_content()` for LLM calls and `models.embed_content()` for RAG embeddings.



streamlit run frontend/app.py 
uvicorn app.main:app --reload --port 8000