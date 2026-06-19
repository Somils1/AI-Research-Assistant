import os

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings


def save_uploaded_pdf(
    uploaded_file
):

    save_path = os.path.join(
        "data",
        uploaded_file.name
    )

    with open(
        save_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    return save_path


def ingest_pdf(
    pdf_path: str
):

    loader = PyPDFLoader(
        pdf_path
    )

    docs = loader.load()

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    )

    chunks = splitter.split_documents(
        docs
    )

    pdf_name = os.path.basename(pdf_path)
    for chunk in chunks:
       chunk.metadata["source"] = pdf_name

    embeddings = (
      HuggingFaceEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
    )

    vector_store = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory=
        "vector_store"

    )

    return vector_store