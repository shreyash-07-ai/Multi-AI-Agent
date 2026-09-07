from app.rag.chunking import chunk_text

def test_chunking():
    chunks = chunk_text("a" * 2000, chunk_size=500, overlap=50)
    assert len(chunks) > 1
