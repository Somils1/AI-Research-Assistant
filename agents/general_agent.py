from langchain_core.tools import tool

from langchain_openai import ChatOpenAI

from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import ToolNode

from graph.state import AgentState
import os

@tool
def calculator(
    expression: str) -> str:
    """
    Evaluate mathematical expressions.
    """

    try:

        return str(
            eval(expression)
        )

    except Exception as e:

        return str(e)

search_tool = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search the web."""
    return search_tool.run(query)


tools = [
    calculator,
    web_search
]




llm = ChatOpenAI(
    model="google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=512
)


llm_with_tools = (
    llm.bind_tools(
        tools
    )
)


def general_agent_node(
    state: AgentState
):

    response = (
        llm_with_tools.invoke(
            state["messages"]
        )
    )

    return {

        "messages": [
            response
        ],

        "active_agent":
        "General Agent"

    }


tool_node = ToolNode(
    tools
)