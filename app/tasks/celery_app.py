from celery import Celery
from app.config import REDIS_URL
celery = Celery("multi_agent_ai", broker=REDIS_URL, backend=REDIS_URL)
celery.conf.task_serializer = "json"
celery.conf.result_serializer = "json"
celery.conf.accept_content = ["json"]
