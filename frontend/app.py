import streamlit as st
import requests
from pathlib import Path

st.set_page_config(
    page_title="Multi-Agent AI — Document & PPT Generator",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1050px !important;
        margin: 0 auto !important;
        padding: 1.2rem 1.5rem 2rem !important;
    }
    div[data-testid="stHorizontalBlock"] { gap: 0.55rem !important; }
    h1 {
        font-size: 2rem !important;
        text-align: center !important;
        margin-bottom: 0.15rem !important;
    }
    h2, h3 {
        margin-top: 0.55rem !important;
        margin-bottom: 0.45rem !important;
    }
    [data-testid="stCaptionContainer"] {
        text-align: center !important;
        margin-bottom: 0.8rem !important;
    }
    [data-testid="stFileUploader"] { padding: 0.15rem !important; }
    [data-testid="stTextArea"] textarea {
        min-height: 88px !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stTextInput"] input { font-size: 0.9rem !important; }
    .stButton > button, .stDownloadButton > button {
        min-height: 2.25rem !important;
        padding: 0.35rem 0.85rem !important;
        font-size: 0.82rem !important;
        border-radius: 0.45rem !important;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        width: 100% !important;
        max-width: 360px !important;
        display: block !important;
        margin: 0.35rem auto 0 !important;
    }
    [data-testid="stCheckbox"] { padding-top: 0.1rem !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0.7rem 0.9rem !important;
        border-radius: 0.65rem !important;
    }
    .dashboard-note {
        text-align: center;
        font-size: 0.78rem;
        opacity: 0.75;
        margin-top: 0.35rem;
    }
    @media (max-width: 700px) {
        .block-container { padding: 0.8rem 0.75rem 1.5rem !important; }
        h1 { font-size: 1.45rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "file_ids" not in st.session_state:
    st.session_state.file_ids = []
if "uploaded_names" not in st.session_state:
    st.session_state.uploaded_names = []

st.title("Multi-Agent AI — Document & PPT Generator")
st.caption("Developed by Shreyash Musmade")

API = "http://localhost:8000"
with st.expander("⚙️ Backend connection", expanded=False):
    API = st.text_input(
        "FastAPI URL",
        API,
        label_visibility="collapsed",
        placeholder="http://localhost:8000",
    )

with st.container(border=True):
    st.subheader("1. Upload enterprise knowledge and templates")
    files = st.file_uploader(
        "PDF, DOCX, PPTX or image",
        type=["pdf", "docx", "pptx", "png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
    )

    upload_col, count_col = st.columns([1, 1])
    with upload_col:
        upload_clicked = st.button("📥 Upload + Index", use_container_width=True)
    with count_col:
        st.markdown(
            f"<div class='dashboard-note'>Indexed files: <b>{len(st.session_state.uploaded_names)}</b></div>",
            unsafe_allow_html=True,
        )

    if upload_clicked and files:
        for f in files:
            try:
                r = requests.post(
                    f"{API}/upload",
                    files={"file": (f.name, f.getvalue(), f.type)},
                    timeout=180,
                )
                if r.ok:
                    d = r.json()
                    st.session_state.file_ids.append(d["file_id"])
                    st.session_state.uploaded_names.append((f.name, d["file_id"]))
                    st.success(f"{f.name}: indexed {d['chunks']} chunks")
                else:
                    st.error(r.text)
            except requests.RequestException as exc:
                st.error(f"Backend connection failed: {exc}")

    if st.session_state.uploaded_names:
        st.caption("Indexed: " + " • ".join(x[0] for x in st.session_state.uploaded_names))

with st.container(border=True):
    st.subheader("2. Request")
    query = st.text_area(
        "Prompt",
        "Research the latest Generative AI trends and create a proposal and a 12-slide presentation using the same tone and style as the uploaded files.",
        height=90,
    )

    make_col, ppt_col = st.columns(2)
    with make_col:
        make_doc = st.checkbox("Generate editable DOCX", value=True)
    with ppt_col:
        make_ppt = st.checkbox("Generate editable PPTX", value=True)

    run_clicked = st.button("🚀 Run Multi-Agent Workflow", type="primary")

if run_clicked:
    payload = {
        "message": query,
        "session_id": "demo",
        "document_ids": st.session_state.file_ids,
        "generate_docx": make_doc,
        "generate_pptx": make_ppt,
    }

    with st.spinner("Running agents..."):
        try:
            r = requests.post(f"{API}/chat", json=payload, timeout=300)
        except requests.RequestException as exc:
            r = None
            st.error(f"Backend connection failed: {exc}")

    if r is not None:
        if r.ok:
            d = r.json()
            st.success(f"Workflow complete — Version {d['version']}")

            with st.expander("🔎 Agent trace", expanded=False):
                for item in d["trace"]:
                    st.write("•", item)

            with st.expander("✅ Validation", expanded=False):
                st.json(d["validation"])

            if d["sources"]:
                with st.expander("🌐 Web sources", expanded=False):
                    for s in d["sources"]:
                        st.write(f"- [{s['title']}]({s['url']})")

            with st.container(border=True):
                st.subheader("Answer")
                st.write(d["answer"])

            if d["artifacts"]:
                st.subheader("Generated files")
                download_cols = st.columns(min(len(d["artifacts"]), 2))
                for index, (kind, path) in enumerate(d["artifacts"].items()):
                    p = Path(path)
                    if p.exists():
                        with download_cols[index % len(download_cols)]:
                            st.download_button(
                                f"⬇️ Download {kind.upper()}",
                                p.read_bytes(),
                                file_name=p.name,
                                use_container_width=True,
                            )
        else:
            st.error(r.text)
