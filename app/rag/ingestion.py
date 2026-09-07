from pathlib import Path
from app.document_processing.router import extract_text
from .chunking import chunk_text
from .embeddings import embed_texts
from .pinecone_store import PineconeStore

def ingest_file(path, file_id):
    text = extract_text(path)
    chunks = chunk_text(text)
    if not chunks:
        return 0
    vectors = embed_texts(chunks)
    payload = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        payload.append({
            "id": f"{file_id}-{i}",
            "values": vector,
            "metadata": {"file_id": file_id, "chunk_id": i, "text": chunk, "filename": Path(path).name}
        })
    PineconeStore().upsert(payload)
    return len(chunks)
