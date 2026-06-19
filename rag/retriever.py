from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = (
        HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    )

vector_store = Chroma(

        persist_directory=
        "vector_store",

        embedding_function=
        embeddings
    )


def get_retriever(pdf_name):


    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k":10,
            "filter": {
            "source": pdf_name}
        },
    )


def get_retrieval_preview(
    query: str,
    pdf_name: str) -> str:
    
    if not pdf_name:
        return ""

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 2,
            "filter": {
                "source": pdf_name
            }
        }
    )

    docs = retriever.invoke(query)

    if not docs:
        return ""

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )