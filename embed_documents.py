"""
Embed all PDF/DOCX files from the documents/ folder into ChromaDB.
Place your documents in the 'documents/' folder and run this script.
"""
import os
import sys
import io
import uuid
from pathlib import Path
from typing import List

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Disable symlinks for Windows compatibility
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

import chromadb
from chromadb.config import Settings
from docling.document_converter import DocumentConverter

from ollama_client import OllamaEmbeddingFunction
from rag_config import paths


RAW_DOCS = "documents/raw_documents"
PROCESSED_DOCS = "documents/processed_documents"
VECTOR_DATA = "documents/vector_data"


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


def embed_all_documents():
    """Convert and embed all PDF/DOCX files from raw_documents/ folder."""
    
    # Ensure directories exist
    Path(RAW_DOCS).mkdir(parents=True, exist_ok=True)
    Path(PROCESSED_DOCS).mkdir(parents=True, exist_ok=True)
    Path(VECTOR_DATA).mkdir(parents=True, exist_ok=True)
    
    # Initialize ChromaDB in vector_data folder
    client = chromadb.PersistentClient(
        path=VECTOR_DATA,
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=OllamaEmbeddingFunction(),
    )
    
    # Find all PDF and DOCX files in raw_documents
    doc_files = list(Path(RAW_DOCS).glob("*.pdf")) + list(Path(RAW_DOCS).glob("*.docx"))
    
    if not doc_files:
        print(f"No PDF or DOCX files found in '{RAW_DOCS}/' folder.")
        print(f"Please place your documents in '{RAW_DOCS}/' and run again.")
        return
    
    print(f"Found {len(doc_files)} document(s) to process...")
    
    converter = DocumentConverter()
    total_embedded = 0
    
    for doc_path in doc_files:
        print(f"\nProcessing: {doc_path.name}")
        
        # Convert to markdown
        result = converter.convert(str(doc_path))
        markdown_text = result.document.export_to_markdown()
        
        # Save markdown to processed_documents
        md_path = Path(PROCESSED_DOCS) / f"{doc_path.stem}.md"
        md_path.write_text(markdown_text, encoding="utf-8")
        print(f"  -> Saved to: {md_path}")
        
        # Chunk and embed into ChromaDB
        if markdown_text.strip():
            chunks = chunk_text(markdown_text)
            ids = [str(uuid.uuid4()) for _ in chunks]
            metadatas = [{"source": str(md_path), "original_file": doc_path.name, "chunk": i} for i in range(len(chunks))]
            
            collection.add(
                ids=ids,
                documents=chunks,
                metadatas=metadatas
            )
            total_embedded += len(chunks)
            print(f"  -> Embedded {len(chunks)} chunks into ChromaDB")
    
    print(f"\n[OK] Successfully embedded {total_embedded} document(s)!")
    print(f"  Raw documents: {RAW_DOCS}")
    print(f"  Processed (markdown): {PROCESSED_DOCS}")
    print(f"  Vector database: {VECTOR_DATA}")


if __name__ == "__main__":
    embed_all_documents()
