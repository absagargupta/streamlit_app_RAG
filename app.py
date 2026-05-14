import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from src.pdf_processor import load_and_split_pdf
from src.vector_store import create_vector_store
from src.rag_pipeline import generate_answer

# =========================
# Load Environment Variables
# =========================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found.")
    st.stop()

# =========================
# Streamlit UI
# =========================

st.set_page_config(
    page_title="Document Q&A App"
)

st.title("📄 Document Q&A App")

st.write(
    "Upload a PDF and ask questions about it."
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# =========================
# Process PDF
# =========================

if uploaded_file is not None:

    if (
        "uploaded_filename"
        not in st.session_state
        or st.session_state.uploaded_filename
        != uploaded_file.name
    ):

        with st.spinner("Processing PDF..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.read()
                )

                temp_pdf_path = tmp_file.name

            split_documents = load_and_split_pdf(
                temp_pdf_path
            )

            vector_store = create_vector_store(
                split_documents,
                OPENAI_API_KEY
            )

            st.session_state.vector_store = (
                vector_store
            )

            st.session_state.uploaded_filename = (
                uploaded_file.name
            )

            os.remove(temp_pdf_path)

        st.success(
            f"{uploaded_file.name} processed successfully!"
        )

# =========================
# Question Answering
# =========================

if "vector_store" in st.session_state:

    question = st.text_input(
        "Ask a question about the document"
    )

    if question:

        with st.spinner("Generating answer..."):

            answer, retrieved_docs = (
                generate_answer(
                    question,
                    st.session_state.vector_store,
                    OPENAI_API_KEY
                )
            )

            st.subheader("Answer")

            st.write(answer)

            st.subheader("Sources")

            displayed_sources = set()

            for doc in retrieved_docs:

                source = os.path.basename(
                    doc.metadata.get(
                        "source",
                        "Unknown"
                    )
                )

                page = doc.metadata.get(
                    "page",
                    "Unknown"
                )

                source_text = (
                    f"- {source} (Page {page + 1})"
                )

                if source_text not in displayed_sources:

                    st.write(source_text)

                    displayed_sources.add(
                        source_text
                    )