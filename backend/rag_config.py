import os
from dataclasses import dataclass


@dataclass
class OllamaConfig:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "mistral")
    embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


@dataclass
class Paths:
    base_dir: str = "documents"
    raw_dir: str = os.path.join("documents", "raw_documents")
    processed_dir: str = os.path.join("documents", "processed_documents")
    vector_db_dir: str = os.path.join("documents", "vector_data")


ollama_config = OllamaConfig()
paths = Paths()


