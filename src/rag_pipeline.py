from openai import OpenAI

from src.prompts import QA_PROMPT_TEMPLATE
from src.config import (
    TOP_K_RESULTS,
    LLM_MODEL, TEMPERATURE
)

def generate_answer(
    question,
    vector_store,
    openai_api_key
):

    retriever = vector_store.as_retriever(
        search_kwargs={"k": TOP_K_RESULTS}
    )

    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        return (
            "I could not find relevant information in the uploaded documents.",
            []
        )    

    context = "\n\n".join([
        f"Document Chunk {idx + 1}:\n{doc.page_content}"
        for idx, doc in enumerate(retrieved_docs)
    ])

    prompt = QA_PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE
    )

    answer = response.choices[0].message.content

    return answer, retrieved_docs