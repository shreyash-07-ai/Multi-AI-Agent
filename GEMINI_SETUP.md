# Gemini API setup

This repository is configured for **Gemini only**. You do not need an OpenAI API key.

## 1. Create `.env`

Windows PowerShell:

```powershell
copy .env.example .env
```

Then edit `.env`:

```env
GEMINI_API_KEY=YOUR_GEMINI_KEY
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSION=768

PINECONE_API_KEY=YOUR_PINECONE_KEY
PINECONE_INDEX=multi-agent-rag-gemini
```

## 2. Install

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Run

Terminal 1:

```powershell
uvicorn app.main:app --reload --port 8000
```

Terminal 2:

```powershell
streamlit run frontend/app.py
```

Redis is only needed when you run the Celery worker:

```powershell
celery -A app.tasks.celery_app.celery worker --loglevel=INFO
```

## Important Pinecone change

The previous OpenAI version used a 64-dimensional OpenAI embedding. This Gemini version uses `gemini-embedding-001` with 768 dimensions.

**Do not reuse the old 64-dimensional Pinecone index.** The code uses:

```env
PINECONE_INDEX=multi-agent-rag-gemini
```

so Pinecone can create/use a correctly sized index.

## What changed

- `app/agents/llm.py` -> Google GenAI SDK
- `app/rag/embeddings.py` -> Gemini embeddings
- `app/config.py` -> `GEMINI_API_KEY`, Gemini model settings
- `requirements.txt` -> `google-genai`, no `openai`
- `.env.example` -> Gemini variables
- RAG embedding dimension -> 768

Google's current Python examples use `from google import genai`, `client.models.generate_content(...)`, and `client.models.embed_content(...)`.
