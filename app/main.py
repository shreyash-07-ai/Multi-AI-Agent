from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.artifacts import router as artifacts_router
from app.api.versions import router as versions_router

app = FastAPI(title="Multi-Agent AI Document & PPT Generator", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(artifacts_router)
app.include_router(versions_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "multi-agent-ai"}
