import json
from typing import List

import requests

from rag_config import ollama_config


class OllamaEmbeddingFunction:
    """
    Custom embedding function for ChromaDB that calls Ollama's /embeddings endpoint.
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
        url = f"{ollama_config.base_url}/api/embed"
        embeddings: List[List[float]] = []
        for text in input:
            payload = {"model": ollama_config.embed_model, "input": text}
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            # Ollama /api/embed returns {"embeddings": [[...]]}
            if "embeddings" in data:
                emb = data["embeddings"][0]
                if not isinstance(emb, list):
                    raise TypeError(f"Expected list, got {type(emb)}")
                embeddings.append(emb)
            elif "embedding" in data:
                emb = data["embedding"]
                if not isinstance(emb, list):
                    raise TypeError(f"Expected list, got {type(emb)}")
                embeddings.append(emb)
            else:
                raise ValueError(f"Unexpected response format: {data}")
        return embeddings


def ollama_chat(messages: List[dict]) -> str:
    """
    Call Ollama chat endpoint with a list of messages and return the assistant reply text.
    """
    url = f"{ollama_config.base_url}/api/chat"
    payload = {
        "model": ollama_config.chat_model,
        "messages": messages,
        "stream": False,
    }
    resp = requests.post(url, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    # Ollama chat response structure: {"message": {"role": "assistant", "content": "..."}}
    return data["message"]["content"]


def ollama_generate(prompt: str) -> str:
    """
    Call Ollama generate endpoint with a prompt and return the response.
    """
    url = f"{ollama_config.base_url}/api/generate"
    payload = {
        "model": ollama_config.chat_model,
        "prompt": prompt,
        "stream": False,
    }
    resp = requests.post(url, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    return data["response"].strip()


