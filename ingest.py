import os
import uuid
from pathlib import Path
from typing import List, Tuple

import chromadb
from chromadb.config import Settings
from docling.document_converter import DocumentConverter

from ollama_client import OllamaEmbeddingFunction
from rag_config import paths


def ensure_dirs() -> None:
    Path(paths.data_dir).mkdir(parents=True, exist_ok=True)
    Path(paths.markdown_dir).mkdir(parents=True, exist_ok=True)
    Path(paths.chroma_dir).mkdir(parents=True, exist_ok=True)


def init_chroma():
    client = chromadb.PersistentClient(
        path=paths.chroma_dir,
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=OllamaEmbeddingFunction(),
    )
    return client, collection


def convert_to_markdown(input_path: str) -> Tuple[str, str]:
    """
    Use Docling to convert PDF/DOCX to markdown and save to markdown_dir.
    Returns (markdown_path, markdown_content).
    """
    converter = DocumentConverter()
    result = converter.convert(input_path)
    md = result.document.export_to_markdown()

    base_name = Path(input_path).stem
    md_filename = f"{base_name}.md"
    md_path = str(Path(paths.markdown_dir) / md_filename)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    return md_path, md


def index_markdown_files(filepaths: List[str] | None = None) -> int:
    """
    Index markdown files into ChromaDB.
    If filepaths is None, index all .md files in markdown_dir.
    Returns number of documents added.
    """
    _, collection = init_chroma()

    if filepaths is None:
        filepaths = [
            str(p)
            for p in Path(paths.markdown_dir).glob("*.md")
            if p.is_file()
        ]

    ids: List[str] = []
    docs: List[str] = []
    metadatas: List[dict] = []

    for md_path in filepaths:
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()
        if not text.strip():
            continue
        doc_id = str(uuid.uuid4())
        ids.append(doc_id)
        docs.append(text)
        metadatas.append(
            {
                "source": md_path,
            }
        )

    if not ids:
        return 0

    collection.add(ids=ids, documents=docs, metadatas=metadatas)
    return len(ids)


def ingest_file(file_path: str) -> int:
    """
    Convert a single PDF/DOCX to markdown and index it.
    Returns number of records added.
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
        folder = paths.data_dir
    exts = {".pdf", ".docx"}
    files = [
        str(p)
        for p in Path(folder).glob("*")
        if p.is_file() and p.suffix.lower() in exts
    ]
    if not files:
        return 0

    md_paths: List[str] = []
    for fpath in files:
        md_path, _ = convert_to_markdown(fpath)
        md_paths.append(md_path)

    return index_markdown_files(md_paths)


if __name__ == "__main__":
    ensure_dirs()
    added = ingest_folder()
    print(f"Ingested {added} documents into ChromaDB.")


