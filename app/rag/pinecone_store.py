from pinecone import Pinecone, ServerlessSpec
from app.config import (
    PINECONE_API_KEY, PINECONE_INDEX, PINECONE_NAMESPACE,
    PINECONE_CLOUD, PINECONE_REGION, EMBEDDING_DIMENSION
)

class PineconeStore:
    def __init__(self):
        if not PINECONE_API_KEY:
            raise RuntimeError("PINECONE_API_KEY is missing in .env")
        if not PINECONE_INDEX:
            raise RuntimeError("PINECONE_INDEX is missing in .env")
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self._ensure_index()
        self.index = self.pc.Index(PINECONE_INDEX)

    def _ensure_index(self):
        names = [x["name"] for x in self.pc.list_indexes()]
        if PINECONE_INDEX not in names:
            self.pc.create_index(
                name=PINECONE_INDEX,
                dimension=EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
            )
        else:
            info = self.pc.describe_index(PINECONE_INDEX)
            dimension = getattr(info, "dimension", None)
            if dimension is None and isinstance(info, dict):
                dimension = info.get("dimension")
            if dimension and int(dimension) != EMBEDDING_DIMENSION:
                raise RuntimeError(
                    f"Pinecone index '{PINECONE_INDEX}' has dimension {dimension}; "
                    f"this project requires {EMBEDDING_DIMENSION}. "
                    "Create/recreate the index with the matching dimension."
                )

    def upsert(self, vectors):
        if vectors:
            self.index.upsert(vectors=vectors, namespace=PINECONE_NAMESPACE)

    def query(self, vector, top_k=5):
        return self.index.query(
            vector=vector, top_k=top_k, include_metadata=True,
            namespace=PINECONE_NAMESPACE
        )
