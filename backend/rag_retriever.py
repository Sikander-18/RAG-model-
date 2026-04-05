from typing import List, Tuple
import os
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


def retrieve(query: str, k: int = 12) -> Tuple[List[str], List[dict]]:
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


def generate_answer(query: str, k: int = 12) -> Tuple[str, List[dict]]:
    """Generate an answer using retrieved context and Ollama."""
    docs, metadatas = retrieve(query, k=k)
    
    if not docs:
        return "I cannot find any relevant information in the provided documents to answer your question.", []
    
    # Build a sophisticated context string that includes sources for the AI
    context_parts = []
    for doc, meta in zip(docs, metadatas):
        source_name = meta.get("source", "Unknown Document")
        context_parts.append(f"--- SOURCE: {source_name} ---\n{doc}")
    
    context = "\n\n".join(context_parts)

    prompt = f"""You are a professional RAG (Retrieval-Augmented Generation) assistant. 
Your goal is to provide accurate, well-structured, and helpful answers based ONLY on the provided context below.

### Instructions:
1. If the question asks for names, lists, or projects, provide them in a clear, bulleted or numbered format.
2. Cross-reference information from different sources if they are provided.
3. If the answer is not in the context, state clearly that you cannot find this specific information in the current documents.
4. Maintain a formal, developer-friendly tone.

### Context:
{context}

### Question: {query}

### Answer:"""

    answer = ollama_generate(prompt)
    return answer, metadatas
