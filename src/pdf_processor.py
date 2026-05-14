from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

def load_and_split_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    split_documents = text_splitter.split_documents(
        documents
    )

    return split_documents