from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from graph.state import AgentState
from langchain_openai import ChatOpenAI
from rag.retriever import (
    get_retriever
)

import os

llm = ChatOpenAI(
    model="google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=2048
)

def retriever_agent(
    state: AgentState
):
    pdf_name = state.get('current_pdf',"")

    query = (
        state["messages"][-1]
        .content
    )

    retriever = (
        get_retriever(pdf_name)
    )

    docs = retriever.invoke(
        query
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    response = llm.invoke(
         f"""
    You are a document question-answering assistant.

    Answer the user's question using ONLY the retrieved context.

    Rules:
    1. Do not use outside knowledge.
    2. If the answer is not available in the context, say:
   "I could not find that information in the uploaded document."
    3. Be concise and accurate.

    Retrieved Context:
    {context}

    User Question:
    {query}

    Answer:
    """
    )

    return {

        "messages": [
            response
        ],

        "retrieved_chunks": [
            doc.page_content
            for doc in docs
        ],

        "active_agent":
        "RAG Agent"

    }