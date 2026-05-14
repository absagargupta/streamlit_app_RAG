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

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 3:
    st.error("Please upload a maximum of 3 PDFs.")
    st.stop()
# =========================
# Process PDF
# =========================

if uploaded_files:

    current_filenames = sorted(
        [file.name for file in uploaded_files]
    )

    if (
        "uploaded_filenames"
        not in st.session_state
        or st.session_state.uploaded_filenames
        != current_filenames
    ):

        with st.spinner("Processing PDFs..."):

            all_documents = []

            for uploaded_file in uploaded_files:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp_file:

                    tmp_file.write(
                        uploaded_file.read()
                    )

                    temp_pdf_path = tmp_file.name

                split_documents = (
                    load_and_split_pdf(
                        temp_pdf_path
                    )
                )

                for doc in split_documents:
                    doc.metadata["source"] = uploaded_file.name



                all_documents.extend(
                    split_documents
                )

                os.remove(temp_pdf_path)

            vector_store = create_vector_store(
                all_documents,
                OPENAI_API_KEY
            )

            st.session_state.vector_store = (
                vector_store
            )

            st.session_state.uploaded_filenames = (
                current_filenames
            )

        st.success(
            f"{len(uploaded_files)} PDFs processed successfully!"
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
## Citation
            st.subheader("Sources")

            unique_sources = sorted(set([
                (
                    os.path.basename(
                        doc.metadata.get(
                            "source",
                            "Unknown"
                        )
                    ),
                    doc.metadata.get(
                        "page",
                        "Unknown"
                    )
                )
                for doc in retrieved_docs
            ]))

            for source, page in unique_sources:

                st.write(
                    f"- {source} (Page {page + 1 if isinstance(page, int) else page})"
                )
# Retrieval Transparency
            with st.expander("Retrieved Context"):

                for idx, doc in enumerate(
                    retrieved_docs,
                    start=1
                ):

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

                    st.markdown(
                        f"### Chunk {idx}"
                    )

                    st.write(
                        f"Source: {source}"
                    )

                    st.write(
                        f"Page: {page + 1}"
                    )

                    st.write(doc.page_content)

                    st.divider()