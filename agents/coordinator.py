from typing import Literal

from pydantic import BaseModel

from langchain_openai import ChatOpenAI

from graph.state import AgentState

from rag.retriever import get_retrieval_preview

import os

llm = ChatOpenAI(
    model="google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=512
)


class RouteDecision(BaseModel):
    route: Literal[
        "retriever",
        "general"
    ]


router_llm = llm.with_structured_output(
    RouteDecision
)


ROUTER_PROMPT = """
You are a coordinator agent.

User Query:
{query}

Retrieved Context:
{context}

If the retrieved context contains enough information
to answer the query, route to 'retriever'.

If the retrieved context is empty, irrelevant,
or insufficient, route to 'general'.

Respond only with:

retriever

or

general
"""


def coordinator_node(
    state: AgentState
):

    query = state["messages"][-1].content
    pdf_name = state.get("current_pdf","")

    preview = get_retrieval_preview(
        query=query,
        pdf_name=pdf_name
    )

    response = router_llm.invoke(
        ROUTER_PROMPT.format(
            query=query,
            context=preview
        )
    )

    return {
        "route": response.route
    }