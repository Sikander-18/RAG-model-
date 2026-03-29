from typing import List, Tuple

import chromadb
from chromadb.config import Settings

from ollama_client import ollama_generate, OllamaEmbeddingFunction
from rag_config import paths


def get_collection():
    """Get the ChromaDB collection using unified paths."""
    client = chromadb.PersistentClient(
        path=paths.vector_db_dir,
        settings=Settings(anonymized_telemetry=False),
    )
    # Get or create collection with its stored embedding function
    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=OllamaEmbeddingFunction(),
    )
    return collection


def retrieve(query: str, k: int = 4) -> Tuple[List[str], List[dict]]:
    """Retrieve relevant document chunks from the vector database."""
    collection = get_collection()
    
    # Manually compute query embedding
    embed_fn = OllamaEmbeddingFunction()
    query_embedding = embed_fn.embed_query(query)
    
    # Query using embeddings directly
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    docs = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    return docs, metadatas


def generate_answer(query: str, k: int = 4) -> Tuple[str, List[dict]]:
    """Generate an answer using retrieved context and Ollama."""
    docs, metadatas = retrieve(query, k=k)
    
    if not docs:
        return "I cannot find any relevant information in the provided documents to answer your question.", []
    
    context = "\n\n".join(docs)

    prompt = f"""You are an offline AI assistant. Use ONLY the context below to answer the user's question accurately. If the answer is not in the context, say "I cannot find this information in the provided documents."

Context:
{context}

Question: {query}

Answer:"""

    answer = ollama_generate(prompt)
    return answer, metadatas
