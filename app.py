#Phase 1:

# app.py


import os
import tempfile


import streamlit as st
from dotenv import load_dotenv


from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


from openai import OpenAI


# =========================
# Load Environment Variables
# =========================


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
   st.error("OPENAI_API_KEY not found in environment.")
   st.stop()


# =========================
# OpenAI Client
# =========================


client = OpenAI(api_key=OPENAI_API_KEY)


# =========================
# Streamlit UI
# =========================


st.set_page_config(page_title="Document Q&A App")


st.title("📄 Document Q&A App")


st.write("Upload a PDF and ask questions about it.")


uploaded_file = st.file_uploader(
   "Upload PDF",
   type=["pdf"]
)


# =========================
# Process PDF
# =========================


if uploaded_file is not None:

    # Reprocess only if a new PDF is uploaded
    if (
        "uploaded_filename" not in st.session_state
        or st.session_state.uploaded_filename != uploaded_file.name
    ):


       with st.spinner("Processing PDF..."):


           # Save uploaded file temporarily
           with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
               tmp_file.write(uploaded_file.read())
               temp_pdf_path = tmp_file.name


           # Load PDF
           loader = PyPDFLoader(temp_pdf_path)
           documents = loader.load()


           # Split text into chunks
           text_splitter = RecursiveCharacterTextSplitter(
               chunk_size=800,
               chunk_overlap=150
           )


           split_documents = text_splitter.split_documents(documents)


           # Create embeddings
           embeddings = OpenAIEmbeddings(
               model="text-embedding-3-small",
               api_key=OPENAI_API_KEY
           )


           # Create in-memory Chroma vector store
           vector_store = Chroma.from_documents(
               documents=split_documents,
               embedding=embeddings
           )


           # Save to session state
           st.session_state.vector_store = vector_store
           st.session_state.uploaded_filename = uploaded_file.name


           # Cleanup temp file
           os.remove(temp_pdf_path)


       st.success("PDF processed successfully!")


# =========================
# Question Input
# =========================


if "vector_store" in st.session_state:


   question = st.text_input("Ask a question about the document")


   if question:


       with st.spinner("Generating answer..."):


           # Retrieve relevant chunks
           retriever = st.session_state.vector_store.as_retriever(
               search_kwargs={"k": 4}
           )


           retrieved_docs = retriever.invoke(question)


           # Build context
           context = "\n\n".join([
               doc.page_content for doc in retrieved_docs
           ])


           # Prompt
           prompt = f"""
You are a helpful assistant answering questions based ONLY on the provided document context.


If the answer is not available in the context, say:
"I could not find the answer in the provided documents."


Context:
{context}


Question:
{question}


Answer:
"""


           # LLM call
           response = client.chat.completions.create(
               model="gpt-4o-mini",
               messages=[
                   {
                       "role": "user",
                       "content": prompt
                   }
               ],
               temperature=0
           )


           answer = response.choices[0].message.content


           # =========================
           # Display Answer
           # =========================


           st.subheader("Answer")
           st.write(answer)


           # =========================
           # Citations
           # =========================


           st.subheader("Sources")


           displayed_sources = set()


           for doc in retrieved_docs:


               source = os.path.basename(
                   doc.metadata.get("source", "Unknown")
               )


               page = doc.metadata.get("page", "Unknown")


               source_text = f"- {source} (Page {page + 1})"


               if source_text not in displayed_sources:
                   st.write(source_text)
                   displayed_sources.add(source_text)

