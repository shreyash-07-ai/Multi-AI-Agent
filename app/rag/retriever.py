from .embeddings import embed_query
from .pinecone_store import PineconeStore

def retrieve(query, top_k=5):
    result = PineconeStore().query(embed_query(query), top_k=top_k)
    matches = getattr(result, "matches", None)
    if matches is None and isinstance(result, dict):
        matches = result.get("matches", [])
    return [
        {
            "score": getattr(m, "score", m.get("score", 0) if isinstance(m, dict) else 0),
            "text": (getattr(m, "metadata", {}) or {}).get("text", ""),
            "file_id": (getattr(m, "metadata", {}) or {}).get("file_id", ""),
            "filename": (getattr(m, "metadata", {}) or {}).get("filename", ""),
            "chunk_id": (getattr(m, "metadata", {}) or {}).get("chunk_id", ""),
        }
        for m in (matches or [])
    ]
