from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import EMBEDDING_MODEL

def create_vector_store(
    documents,
    openai_api_key
):

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=openai_api_key
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vector_store