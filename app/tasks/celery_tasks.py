from .celery_app import celery
from app.rag.ingestion import ingest_file

@celery.task(name="rag.ingest_file")
def ingest_file_task(path, file_id):
    return ingest_file(path, file_id)
