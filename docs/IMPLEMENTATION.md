# Implementation Notes

The project is intentionally Docker-free. It is designed so the normal demo path only requires:
1. Python dependencies
2. Gemini API key
3. Pinecone API key

Redis/Celery are included because they are part of the requested enterprise architecture; the UI uses synchronous ingestion for a simple local POC and can switch ingestion to the Celery task in deployment.

The template generators preserve the uploaded presentation dimensions/layout collection and DOCX styles. They generate editable native office files rather than PDFs or images.
