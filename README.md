# 🤖 Multi-Agent AI Document & PPT Generator

An AI-powered **Multi-Agent application** that can analyze documents, perform web research, retrieve information using RAG, and generate editable **DOCX documents and PPTX presentations**.

The project uses **Google Gemini**, **Pinecone**, **FastAPI**, and **Streamlit**, with specialized AI agents responsible for different stages of the workflow.

---

## 🚀 Key Features

* 🤖 Multi-Agent AI architecture
* 🎯 Supervisor / Orchestrator Agent
* 🧠 Google Gemini LLM
* 🔎 Retrieval-Augmented Generation (RAG)
* 🗄️ Pinecone Vector Database
* 🌐 Web Research Agent
* 📄 PDF document analysis
* 📝 DOCX document analysis
* 📊 PPTX presentation analysis
* 🖼️ Image processing
* 🔤 OCR using Tesseract
* 📑 Editable DOCX generation
* 📽️ Editable PPTX generation
* 🎨 Template/style preservation
* ✏️ Conversational editing foundation
* ✅ Generated artifact validation
* 📚 Source/citation tracking
* 🔢 Version management
* ⚡ Celery + Redis background task integration
* 🚀 FastAPI backend
* 🖥️ Streamlit frontend

---

# 🏗️ System Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │   Streamlit UI  │
                  │  frontend/app.py│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   FastAPI API   │
                  │    app/main.py  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────────┐
                  │ Supervisor Agent    │
                  │   Orchestrator      │
                  └─────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
 │  Document    │    │ Web Research │    │  RAG Agent   │
 │ Analysis     │    │    Agent     │    │              │
 └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
        │                   │                   │
        │                   │                   ▼
        │                   │             ┌────────────┐
        │                   │             │  Pinecone  │
        │                   │             └────────────┘
        │                   │
        └───────────────────┼────────────────────┘
                            ▼
                  ┌─────────────────────┐
                  │ Generation Agent    │
                  └─────────┬───────────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
          ┌──────────────┐      ┌──────────────┐
          │ DOCX Output  │      │ PPTX Output  │
          └──────┬───────┘      └──────┬───────┘
                 │                     │
                 └──────────┬──────────┘
                            ▼
                  ┌─────────────────────┐
                  │ Validation Agent    │
                  └─────────┬───────────┘
                            ▼
                       Final Output
```

---

# 🧠 AI Agents

The project is divided into specialized agents.

### 1. Supervisor Agent

Acts as the main orchestrator.

Responsibilities:

* Understand user requirements
* Decide which agents are required
* Coordinate the workflow
* Combine results from different agents
* Control the generation pipeline

---

### 2. Document Analysis Agent

Analyzes uploaded documents.

Supported formats:

* PDF
* DOCX
* PPTX
* Images

It extracts useful information that can be passed to other agents.

---

### 3. PPT Analysis Agent

Specialized agent for analyzing PowerPoint presentations.

It can extract information such as:

* Slide structure
* Titles
* Text
* Layout information
* Presentation style
* Existing content

This information helps generate presentations that follow the uploaded template.

---

### 4. Web Research Agent

Performs web research to obtain current information.

The research results can be used during content generation and can also be used for source/citation tracking.

---

### 5. RAG Agent

Implements Retrieval-Augmented Generation.

The pipeline is:

```text
Documents
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
Gemini Embeddings
    │
    ▼
Pinecone
    │
    ▼
Similarity Search
    │
    ▼
Relevant Context
    │
    ▼
Gemini
```

---

### 6. Generation Agent

Responsible for generating the final content.

It supports:

* Business documents
* Proposals
* Reports
* Presentations
* Other structured outputs

---

### 7. Editing Agent

Provides the foundation for conversational editing.

Example:

```text
User:
"Change the executive summary and add two more slides."

        ↓

Editing Agent

        ↓

Updated Artifact
```

---

### 8. Validation Agent

Validates generated artifacts before they are returned to the user.

---

# 📁 Project Structure

```text
Multi-AI-Agent/
│
├── app/
│   │
│   ├── agents/
│   │   ├── document_analysis_agent.py
│   │   ├── editing_agent.py
│   │   ├── generation_agent.py
│   │   ├── llm.py
│   │   ├── ppt_analysis_agent.py
│   │   ├── rag_agent.py
│   │   ├── supervisor_agent.py
│   │   ├── validation_agent.py
│   │   └── web_research_agent.py
│   │
│   ├── api/
│   │   ├── artifacts.py
│   │   ├── chat.py
│   │   ├── upload.py
│   │   └── versions.py
│   │
│   ├── document_processing/
│   │   ├── docx_processor.py
│   │   ├── image_processor.py
│   │   ├── ocr_processor.py
│   │   ├── pdf_processor.py
│   │   ├── pptx_processor.py
│   │   └── router.py
│   │
│   ├── generation/
│   │   ├── converter.py
│   │   ├── docx_generator.py
│   │   └── pptx_generator.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── samples/
│   ├── Enterprise_Knowledge.pdf
│   ├── Company_Proposal_Template.docx
│   └── Company_Presentation_Template.pptx
│
├── .env.example
├── .gitignore
├── GEMINI_SETUP.md
├── requirements.txt
└── README.md
```

---

# 🛠️ Tech Stack

| Category             | Technology               |
| -------------------- | ------------------------ |
| Programming Language | Python                   |
| Frontend             | Streamlit                |
| Backend              | FastAPI                  |
| LLM                  | Google Gemini            |
| Embeddings           | Gemini Embedding         |
| Vector Database      | Pinecone                 |
| RAG                  | Custom RAG Pipeline      |
| OCR                  | Tesseract / pytesseract  |
| PDF Processing       | PyMuPDF                  |
| DOCX Processing      | python-docx              |
| PPTX Processing      | python-pptx              |
| Image Processing     | Pillow                   |
| Web Research         | Requests + BeautifulSoup |
| Background Jobs      | Celery                   |
| Message Broker       | Redis                    |
| Validation           | Pydantic                 |
| DOCX Generation      | python-docx              |
| PPTX Generation      | python-pptx              |

---

# 🔑 Environment Configuration

Create a `.env` file using `.env.example`.

```env
# Gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash

# Embeddings
EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSION=768

# Pinecone
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX=multi-agent-rag-gemini
PINECONE_NAMESPACE=default
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

# Optional
XAI_API_KEY=
XAI_MODEL=grok-4.6

# Redis
REDIS_URL=redis://localhost:6379/0

# Application directories
DATA_DIR=./data
UPLOAD_DIR=./uploads
OUTPUT_DIR=./outputs

WEB_MAX_RESULTS=5
```

### Important

Do **not** commit your `.env` file to GitHub.

Only commit:

```text
.env.example
```

---

# 📦 Installation

## 1. Clone Repository

```bash
git clone https://github.com/shreyash-07-ai/Multi-AI-Agent.git
```

```bash
cd Multi-AI-Agent
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure Environment

```powershell
copy .env.example .env
```

Open `.env` and add:

```env
GEMINI_API_KEY=your-key
PINECONE_API_KEY=your-key
```

---

# ▶️ Run the Application

The application contains two main services:

```text
Streamlit Frontend
        │
        ▼
FastAPI Backend
```

Both need to be running for the complete local workflow.

---

## Terminal 1 — FastAPI Backend

Activate the environment:

```powershell
.venv\Scripts\activate
```

Run:

```powershell
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "multi-agent-ai"
}
```

---

## Terminal 2 — Streamlit Frontend

Activate the environment:

```powershell
.venv\Scripts\activate
```

Run:

```powershell
streamlit run frontend/app.py
```

Streamlit normally runs at:

```text
http://localhost:8501
```

---

# ⚡ Celery + Redis

Celery and Redis are included for background/asynchronous processing.

Start Redis first.

Then run:

```powershell
celery -A app.tasks.celery_app.celery worker --loglevel=INFO
```

For the basic demo workflow, ingestion can run synchronously without a Celery worker.

---

# 🧪 Test the Application

Sample files are included in:

```text
samples/
```

Example files:

```text
Enterprise_Knowledge.pdf
Company_Proposal_Template.docx
Company_Presentation_Template.pptx
```

Upload these files through Streamlit.

Then try a request such as:

```text
Research the latest Generative AI trends and create a proposal and a 12-slide presentation using the same tone and style as the uploaded files.
```

The system can:

```text
Upload Files
     ↓
Analyze Files
     ↓
Research Web
     ↓
Retrieve RAG Context
     ↓
Generate Content
     ↓
Generate DOCX + PPTX
     ↓
Validate Output
     ↓
Download Files
```

---

# 📄 Supported Input Formats

| Format | Purpose                        |
| ------ | ------------------------------ |
| PDF    | Knowledge/reference documents  |
| DOCX   | Document/template analysis     |
| PPTX   | Presentation/template analysis |
| Images | Image/OCR processing           |

---

# 📤 Generated Outputs

The system generates editable files.

### DOCX

Generated using:

```text
python-docx
```

Output can contain:

* Headings
* Paragraphs
* Tables
* Structured sections
* References/sources

### PPTX

Generated using:

```text
python-pptx
```

Output can contain:

* Titles
* Text
* Multiple slides
* Template-based layouts
* Structured presentation content

---

# 🔤 OCR Pipeline

For scanned documents/images:

```text
Image / Scanned PDF
        ↓
Image Processing
        ↓
Tesseract OCR
        ↓
Extracted Text
        ↓
AI Processing
```

Python dependency:

```text
pytesseract
```

Tesseract OCR must also be installed on the system.

---

# 🌐 Web Research

The Web Research Agent uses:

```text
Requests
+
BeautifulSoup
```

to retrieve and parse online information.

The information can then be passed to the generation pipeline.

---

# 🔎 RAG Configuration

The project uses Gemini embeddings with Pinecone.

Current configuration:

```env
EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSION=768
```

Pinecone:

```env
PINECONE_INDEX=multi-agent-rag-gemini
```

RAG workflow:

```text
Upload Document
      ↓
Extract Text
      ↓
Create Chunks
      ↓
Generate Embeddings
      ↓
Store in Pinecone
      ↓
User Query
      ↓
Similarity Search
      ↓
Retrieve Relevant Chunks
      ↓
Gemini
      ↓
Final Answer
```

---

# 🔌 API

The FastAPI backend provides API modules for:

### Upload

```text
/upload
```

Handles uploaded files and ingestion.

### Chat

```text
/chat
```

Handles user queries and the multi-agent workflow.

### Artifacts

```text
/artifacts
```

Handles generated artifacts.

### Versions

```text
/versions
```

Handles version-related operations.

### Health

```text
/health
```

Used to verify that the backend is running.

---

# 🐛 Troubleshooting

## Backend Connection Error

If Streamlit shows:

```text
Connection refused
localhost:8000
```

make sure FastAPI is running:

```powershell
uvicorn app.main:app --reload --port 8000
```

Keep that terminal open.

Then start Streamlit separately:

```powershell
streamlit run frontend/app.py
```

---

## Gemini API Error

Check:

```env
GEMINI_API_KEY=your-valid-key
```

Also verify:

* API key is valid
* Internet connection is available
* Configured Gemini model is available

---

## Pinecone Error

Verify:

```env
PINECONE_API_KEY=your-key
PINECONE_INDEX=multi-agent-rag-gemini
```

Also make sure the Pinecone index dimension matches:

```text
768
```

---

## OCR Error

Make sure Tesseract is installed and available through the system PATH.

The Python package alone is not enough.

---

## Redis/Celery Error

Make sure Redis is running before starting:

```powershell
celery -A app.tasks.celery_app.celery worker --loglevel=INFO
```

If you are only testing the basic application workflow, Celery can be skipped.

---

# 🔐 Security

Never expose API keys in source code.

Use:

```text
.env
```

for secrets.

Do not commit:

```text
.env
```

to GitHub.

Use:

```text
.env.example
```

for sharing required environment variables.

---

# 📊 Assignment Coverage

| Requirement              | Implementation                  |
| ------------------------ | ------------------------------- |
| Multi-Agent Architecture | Supervisor + Specialized Agents |
| Agent Orchestration      | Supervisor Agent                |
| Document Analysis        | PDF/DOCX/PPTX/Image Processors  |
| PPT Analysis             | PPT Analysis Agent              |
| Web Research             | Web Research Agent              |
| RAG                      | Gemini + Pinecone               |
| OCR                      | Tesseract                       |
| Editable DOCX            | python-docx                     |
| Editable PPTX            | python-pptx                     |
| Template Preservation    | Uploaded templates              |
| Conversational Editing   | Editing Agent                   |
| Validation               | Validation Agent                |
| Citations                | Research/source tracking        |
| Version Management       | Version API                     |
| Backend                  | FastAPI                         |
| Frontend                 | Streamlit                       |
| Background Processing    | Celery + Redis                  |

---

# 📚 Documentation

Additional Gemini configuration information:

```text
GEMINI_SETUP.md
```

Environment template:

```text
.env.example
```

Python dependencies:

```text
requirements.txt
```

---

# 👨‍💻 Author

**Shreyash Musmade**

GitHub:

https://github.com/shreyash-07-ai

Repository:

https://github.com/shreyash-07-ai/Multi-AI-Agent

---

#
