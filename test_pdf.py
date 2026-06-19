from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage

from rag.ingest import ingest_pdf
from graph.graph_builder import graph


# Index PDF once
ingest_pdf("data/test.pdf")   # change path if needed


queries = [
    "Summarize the uploaded document",
    "What does the document say about LangGraph?",
    "What is my favorite color?"
]

for query in queries:

    print("\n" + "=" * 60)
    print("QUERY:", query)
    print("=" * 60)

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=query
                )
            ]
        }
    )

    print("\nRoute:")
    print(result["route"])

    print("\nAgent:")
    print(result["active_agent"])

    print("\nAnswer:")
    print(result["final_answer"])

    if result.get("retrieved_chunks"):

        print("\nRetrieved Chunks:")
        for i, chunk in enumerate(
            result["retrieved_chunks"],
            start=1
        ):
            print(f"\nChunk {i}:")
            print(chunk[:300])