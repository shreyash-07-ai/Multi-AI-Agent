from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, EMBEDDING_MODEL, EMBEDDING_DIMENSION
_client = None


def client():
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is missing in .env")
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def embed_texts(texts, task_type="RETRIEVAL_DOCUMENT"):
    if not texts:
        return []

    result = client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=EMBEDDING_DIMENSION,
        ),
    )
    return [list(item.values) for item in result.embeddings]


def embed_query(text):
    return embed_texts([text], task_type="RETRIEVAL_QUERY")[0]
