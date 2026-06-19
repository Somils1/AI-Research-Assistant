from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.prebuilt import (
    tools_condition
)

from graph.state import AgentState

from agents.coordinator import (
    coordinator_node
)

from agents.general_agent import (
    general_agent_node,
    tool_node
)

from agents.retriever_agent import (
    retriever_agent
)

from agents.synthesizer import (
    synthesizer_node
)


builder = StateGraph(
    AgentState
)


# Nodes

builder.add_node(
    "coordinator",
    coordinator_node
)

builder.add_node(
    "general_agent",
    general_agent_node
)

builder.add_node(
    "tool_node",
    tool_node
)

builder.add_node(
    "retriever_agent",
    retriever_agent
)

builder.add_node(
    "synthesizer",
    synthesizer_node
)


# Start

builder.add_edge(
    START,
    "coordinator"
)


# Router

def route_query(
    state: AgentState
):

    return state["route"]


builder.add_conditional_edges(
    "coordinator",
    route_query,
    {
        "retriever": "retriever_agent",
        "general": "general_agent"
    }
)


# Tool Loop

builder.add_conditional_edges(
    "general_agent",
    tools_condition,
    {
        "tools": "tool_node",
        "__end__": "synthesizer"
    }
)

builder.add_edge(
    "tool_node",
    "general_agent"
)


# RAG Path

builder.add_edge(
    "retriever_agent",
    "synthesizer"
)


# Final

builder.add_edge(
    "synthesizer",
    END
)


graph = builder.compile()