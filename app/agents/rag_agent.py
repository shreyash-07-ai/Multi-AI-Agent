from app.rag.retriever import retrieve

def run_rag(query):
    try:
        return retrieve(query, top_k=6)
    except Exception as e:
        return [{"text": "", "error": str(e)}]
