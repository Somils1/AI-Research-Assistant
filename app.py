import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from graph.graph_builder import (
    graph
)

from rag.ingest import (
    save_uploaded_pdf,
    ingest_pdf
)


# Session State Initialization


if "current_pdf" not in st.session_state:
    st.session_state["current_pdf"] = ""

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Page Config

st.set_page_config(
    page_title="AI Research Assistant"
)

st.title(
    "AI Research Assistant"
)


# PDF Upload


uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    if st.session_state["current_pdf"] != uploaded_file.name:

        st.session_state["current_pdf"] = uploaded_file.name

        pdf_path = save_uploaded_pdf(
            uploaded_file
        )

        ingest_pdf(
            pdf_path
        )

        st.success(
            f"{uploaded_file.name} indexed successfully"
        )


# Render Chat History

for message in st.session_state["chat_history"]:

    with st.chat_message(message["role"]):
        st.write(message["content"])
    
        if (
            message["role"] == "assistant"
            and message.get(
                "retrieved_chunks"
            )
        ):

            with st.expander(
                "Retrieved Context"
            ):

                for chunk in message[
                    "retrieved_chunks"
                ]:

                    st.write(chunk)


# Chat Input

query = st.chat_input(
    "Ask a question"
)

if query:

    # Store User Message
    st.session_state["chat_history"].append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.write(query)

    # Build conversation history for graph
    messages = []

    for msg in st.session_state["chat_history"]:

        if msg["role"] == "user":

            messages.append(
                HumanMessage(
                    content=msg["content"]
                )
            )

        else:

            messages.append(
                AIMessage(
                    content=msg["content"]
                )
            )

    # Invoke Graph
    result = graph.invoke(
        {
            "messages": messages,
            "current_pdf": st.session_state["current_pdf"]
        }
    )

    answer = result["final_answer"]

    # Store Assistant Message
    st.session_state["chat_history"].append(
        {
            "role": "assistant",
            "content": answer,
            "retrieved_chunks": result.get("retrieved_chunks",[])
        }
    )

    # Display Assistant Message
    with st.chat_message("assistant"):
     st.write(answer)
     
    if result.get("retrieved_chunks"):

        with st.expander(
            "Retrieved Context"
        ):

            for chunk in result[
                "retrieved_chunks"
            ]:

                st.write(chunk)
    

    