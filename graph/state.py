from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]

    route: str

    active_agent: str

    retrieved_chunks: list[str]

    final_answer: str
    
    current_pdf: str