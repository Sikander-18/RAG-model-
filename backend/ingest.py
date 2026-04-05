import os
# Disable symlinks for Windows compatibility to prevent permission errors
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
import uuid
from pathlib import Path
from typing import List, Tuple

import chromadb
from chromadb.config import Settings
from docling.document_converter import DocumentConverter

from ollama_client import OllamaEmbeddingFunction
from rag_config import paths


def ensure_dirs() -> None:
    """Ensure all required directories exist."""
    Path(paths.base_dir).mkdir(parents=True, exist_ok=True)
    Path(paths.raw_dir).mkdir(parents=True, exist_ok=True)
    Path(paths.processed_dir).mkdir(parents=True, exist_ok=True)
    Path(paths.vector_db_dir).mkdir(parents=True, exist_ok=True)


def init_chroma():
    """Initialize ChromaDB client and collection."""
    client = chromadb.PersistentClient(
        path=paths.vector_db_dir,
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=OllamaEmbeddingFunction(),
    )
    return client, collection


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# Global converter instance to avoid reloading models for every file
_CONVERTER: DocumentConverter = None

def get_converter():
    global _CONVERTER
    if _CONVERTER is None:
        _CONVERTER = DocumentConverter()
    return _CONVERTER


def convert_to_markdown(input_path: str) -> Tuple[str, str]:
    """
    Use Docling to convert PDF/DOCX to markdown and save to processed_dir.
    Returns (markdown_path, markdown_content).
    """
    converter = get_converter()
    result = converter.convert(input_path)
    md = result.document.export_to_markdown()

    base_name = Path(input_path).stem
    md_filename = f"{base_name}.md"
    md_path = str(Path(paths.processed_dir) / md_filename)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    return md_path, md


def index_markdown_files(filepaths: List[str] | None = None) -> int:
    """
    Index markdown files into ChromaDB with chunking.
    If filepaths is None, index all .md files in processed_dir.
    Returns total number of chunks added.
    """
    _, collection = init_chroma()

    if filepaths is None:
        filepaths = [
            str(p)
            for p in Path(paths.processed_dir).glob("*.md")
            if p.is_file()
        ]

    total_chunks = 0
    for md_path in filepaths:
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        if not text.strip():
            continue

        chunks = chunk_text(text)
        ids: List[str] = [str(uuid.uuid4()) for _ in chunks]
        metadatas: List[dict] = [
            {
                "source": Path(md_path).name,
                "full_path": md_path,
                "chunk": i
            }
            for i in range(len(chunks))
        ]

        collection.add(ids=ids, documents=chunks, metadatas=metadatas)
        total_chunks += len(chunks)

    return total_chunks


def ingest_file(file_path: str) -> int:
    """
    Convert a single PDF/DOCX to markdown and index it.
    Returns number of chunks added.
    """
    ensure_dirs()
    md_path, _ = convert_to_markdown(file_path)
    return index_markdown_files([md_path])


def ingest_folder(folder: str | None = None) -> int:
    """
    Convert and index all PDF/DOCX files in a folder.
    """
    ensure_dirs()
    if folder is None:
        folder = paths.raw_dir
    
    exts = {".pdf", ".docx"}
    files = [
        str(p)
        for p in Path(folder).glob("*")
        if p.is_file() and p.suffix.lower() in exts
    ]
    
    if not files:
        return 0

    total_added = 0
    for fpath in files:
        md_path, _ = convert_to_markdown(fpath)
        total_added += index_markdown_files([md_path])

    return total_added


def delete_from_chroma(filename: str) -> None:
    """
    Remove all chunks associated with a specific source filename from ChromaDB.
    """
    _, collection = init_chroma()
    # Delete based on the metadata 'source' field which matches Path(md_path).name
    collection.delete(where={"source": filename})


if __name__ == "__main__":
    ensure_dirs()
    added = ingest_folder()
    print(f"✅ Ingested {added} chunks into ChromaDB.")
