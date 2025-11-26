from typing import List, Tuple

import chromadb
from chromadb.config import Settings

from ollama_client import ollama_chat, ollama_generate, OllamaEmbeddingFunction
from rag_config import paths


def get_collection():
    # Use vector_data folder if it exists, otherwise use default chroma_dir
    import os
    vector_data_path = "documents/vector_data"
    db_path = vector_data_path if os.path.exists(vector_data_path) else paths.chroma_dir
    
    client = chromadb.PersistentClient(
        path=db_path,
        settings=Settings(anonymized_telemetry=False),
    )
    # Get existing collection with its stored embedding function
    try:
        collection = client.get_collection(
            name="documents",
            embedding_function=OllamaEmbeddingFunction(),
        )
    except:
        collection = client.create_collection(
            name="documents",
            embedding_function=OllamaEmbeddingFunction(),
        )
    return collection


def retrieve(query: str, k: int = 4) -> Tuple[List[str], List[dict]]:
    collection = get_collection()
    # Manually compute query embedding
    embed_fn = OllamaEmbeddingFunction()
    query_embedding = embed_fn.embed_query(query)
    # Query using embeddings directly
    result = collection.query(query_embeddings=[query_embedding], n_results=k)
    docs = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    return docs, metadatas


def generate_answer(query: str, k: int = 4) -> Tuple[str, List[dict]]:
    docs, metadatas = retrieve(query, k=k)
    
    if not docs:
        return "No relevant documents found to answer your question.", []
    
    context = "\n\n".join(docs)

    prompt = f"""You are an offline AI assistant. Use ONLY the context below to answer the user's question accurately. If the answer is not in the context, say "I cannot find this information in the provided documents."

Context:
{context}

Question: {query}

Answer:"""

    answer = ollama_generate(prompt)
    return answer, metadatas


