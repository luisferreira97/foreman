import json
import logging
from pathlib import Path

import duckdb
from langchain.docstore.document import Document
from langchain_community.vectorstores import DuckDB
from langchain_huggingface import HuggingFaceEmbeddings

def load_json(path: str) -> dict:
    """
    Load a JSON file and return it as a dictionary.
    
    Args:
        path (str): The path to the JSON file.
        
    Returns:
        dict: The JSON file as a dictionary.
    """
    
    manifest = json.loads(Path(path).read_text())

    return manifest


def generate_documents(docs: dict) -> Document:
    """
    Generate documents from the given dictionary.

    Args:
        docs (dict): The dictionary containing the documents.
    Returns:
        Document: The generated document.
    """

    logging.info("Generating documents from dictionary")
    new_line = "\n"

    documents = [
        Document(
            page_content=f"{table}{': ' if docs[table]['description'] != '' else ''}{docs[table]['description'].split(new_line)[0] if docs[table]['description'] != '' else ''}",
            metadata={
                "table": table,
                "schema": docs[table]["schema"],
                "description": docs[table]["description"],
                "columns": json.dumps(docs[table]["columns"])
            },
        )
        for table in docs
    ]
    logging.info("Successfully generated documents from dictionary")
    return documents


def load_docs_to_vector_store(docs, embeddings, connection):
    vector_store = DuckDB.from_documents(documents, embeddings, connection=connection)
    return vector_store


if __name__ == "__main__":
    docs = load_json('docs.json')
    documents = generate_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = load_docs_to_vector_store(documents, embeddings, connection=duckdb.connect("docs.duckdb"))
    similarity = vector_store.similarity_search("data makers fest", top_k=5)
    print(similarity)