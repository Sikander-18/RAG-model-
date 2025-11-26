import os
from dataclasses import dataclass


@dataclass
class OllamaConfig:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "mistral")
    embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


@dataclass
class Paths:
    # Legacy paths (used by ingest.py for app.py uploads)
    data_dir: str = os.getenv("DATA_DIR", "data")
    markdown_dir: str = os.getenv("MARKDOWN_DIR", "markdown")
    chroma_dir: str = os.getenv("CHROMA_DIR", "chroma_db")


ollama_config = OllamaConfig()
paths = Paths()

# New organized structure (used by embed_documents.py)
RAW_DOCS = "documents/raw_documents"
PROCESSED_DOCS = "documents/processed_documents"
VECTOR_DATA = "documents/vector_data"


