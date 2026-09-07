import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="Multi-Agent AI", layout="wide")
st.title("Multi-Agent AI — Document & PPT Generator")
st.caption("Develop by Shreyash Musmade")

API = st.sidebar.text_input("FastAPI URL", "http://localhost:8000")
if "file_ids" not in st.session_state:
    st.session_state.file_ids = []
if "uploaded_names" not in st.session_state:
    st.session_state.uploaded_names = []

st.subheader("1. Upload enterprise knowledge and templates")
files = st.file_uploader(
    "PDF, DOCX, PPTX or image",
    type=["pdf","docx","pptx","png","jpg","jpeg","webp"],
    accept_multiple_files=True
)

if st.button("Upload + Index") and files:
    for f in files:
        r = requests.post(f"{API}/upload", files={"file": (f.name, f.getvalue(), f.type)}, timeout=180)
        if r.ok:
            d = r.json()
            st.session_state.file_ids.append(d["file_id"])
            st.session_state.uploaded_names.append((f.name, d["file_id"]))
            st.success(f"{f.name}: indexed {d['chunks']} chunks")
        else:
            st.error(r.text)

st.write("Indexed files:", [x[0] for x in st.session_state.uploaded_names])

st.subheader("2. Request")
query = st.text_area(
    "Prompt",
    "Research the latest Generative AI trends and create a proposal and a 12-slide presentation using the same tone and style as the uploaded files.",
    height=120
)

col1, col2 = st.columns(2)
with col1:
    make_doc = st.checkbox("Generate editable DOCX", True)
with col2:
    make_ppt = st.checkbox("Generate editable PPTX", True)

if st.button("Run Multi-Agent Workflow", type="primary"):
    payload = {
        "message": query,
        "session_id": "demo",
        "document_ids": st.session_state.file_ids,
        "generate_docx": make_doc,
        "generate_pptx": make_ppt
    }
    with st.spinner("Running agents..."):
        r = requests.post(f"{API}/chat", json=payload, timeout=300)
    if r.ok:
        d = r.json()
        st.success(f"Workflow complete — Version {d['version']}")
        st.subheader("Agent trace")
        for item in d["trace"]:
            st.write("•", item)
        st.subheader("Validation")
        st.json(d["validation"])
        if d["sources"]:
            st.subheader("Web sources")
            for s in d["sources"]:
                st.write(f"- [{s['title']}]({s['url']})")
        st.subheader("Answer")
        st.write(d["answer"])
        for kind, path in d["artifacts"].items():
            p = Path(path)
            if p.exists():
                st.download_button(f"Download {kind.upper()}", p.read_bytes(), file_name=p.name)
    else:
        st.error(r.text)
