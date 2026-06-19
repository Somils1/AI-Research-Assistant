from graph.state import AgentState


def synthesizer_node(
    state: AgentState
):

    final_answer = (
        state["messages"][-1]
        .content
    )

    return {

        "final_answer":
        final_answer,

        "active_agent":
        state.get(
            "active_agent",
            "Unknown"
        )

    }