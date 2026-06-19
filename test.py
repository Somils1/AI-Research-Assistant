from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage

from graph.graph_builder import graph


result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="Who is Alan Turing?"
            )
        ]
    }
)

print(result)