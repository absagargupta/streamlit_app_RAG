from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def create_vector_store(
    documents,
    openai_api_key
):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=openai_api_key
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vector_store