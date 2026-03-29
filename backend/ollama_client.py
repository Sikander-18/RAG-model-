import json
import requests
from typing import List
from rag_config import ollama_config


class OllamaEmbeddingFunction:
    """
    Custom embedding function for ChromaDB that calls Ollama's /api/embed endpoint.
    """

    def name(self) -> str:
        return "ollama_embeddings"

    def embed_documents(self, input: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return self.__call__(input)

    def embed_query(self, input: str) -> List[float]:
        """Embed a single query text."""
        result = self.__call__([input])[0]
        if not isinstance(result, list):
            raise TypeError(f"Expected list, got {type(result)}: {result}")
        return result

    def __call__(self, input: List[str]) -> List[List[float]]:
        base = ollama_config.base_url.rstrip("/")
        url = f"{base}/api/embed"
        
        payload = {"model": ollama_config.embed_model, "input": input}
        try:
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            
            # Use "embeddings" if available, else "embedding"
            embeddings = data.get("embeddings") or data.get("embedding")
            if not embeddings:
                raise ValueError(f"Ollama response missing embeddings: {data}")
            
            return embeddings
            
        except Exception as e:
            raise RuntimeError(f"Ollama embedding error at {url}: {e}")


def ollama_generate(prompt: str) -> str:
    """
    Call Ollama /api/generate endpoint and return the response text.
    """
    base = ollama_config.base_url.rstrip("/")
    url = f"{base}/api/generate"
    
    payload = {
        "model": ollama_config.chat_model,
        "prompt": prompt,
        "stream": False,
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=300)
        
        # If we get a 404, provide specific troubleshooting 
        if resp.status_code == 404:
            raise RuntimeError(
                f"Ollama endpoint {url} returned 404 (Not Found). \n"
                f"1. Check if model '{ollama_config.chat_model}' is installed (Run: ollama pull {ollama_config.chat_model})\n"
                f"2. Ensure Ollama is running correctly."
            )
            
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Connection issue with Ollama: {e}")


def ollama_chat(messages: List[dict]) -> str:
    """
    Call Ollama /api/chat endpoint and return the reply.
    """
    base = ollama_config.base_url.rstrip("/")
    url = f"{base}/api/chat"
    
    payload = {
        "model": ollama_config.chat_model,
        "messages": messages,
        "stream": False,
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Ollama chat error: {e}")
