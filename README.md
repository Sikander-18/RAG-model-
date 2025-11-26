# Local RAG System (Docling + ChromaDB + Mistral 7B via Ollama)

## Overview

Fully offline RAG pipeline using:
- **Docling** - PDF/DOCX to markdown conversion
- **ChromaDB** - Vector database
- **Ollama** - Local embeddings (nomic-embed-text) & LLM (mistral)
- **Streamlit** - Web UI

## Prerequisites

1. Python 3.10+
2. [Ollama](https://ollama.com) installed
3. Pull models:
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

## Installation

```bash
pip install -r requirements.txt
```

## Folder Structure

```
documents/
├── raw_documents/       ← Put your PDF/DOCX files here
├── processed_documents/ ← Auto-generated markdown files
└── vector_data/         ← Auto-generated ChromaDB vectors
```

## Usage

### 1. Add Documents
Place PDF/DOCX files in `documents/raw_documents/`

### 2. Embed Documents
```bash
python embed_documents.py
```
This will:
- Convert documents to markdown → `processed_documents/`
- Generate embeddings via Ollama
- Store vectors in ChromaDB → `vector_data/`

### 3. Run Streamlit App
```bash
streamlit run app.py
```
Open http://localhost:8501 and ask questions!

## Configuration

Edit `rag_config.py` or set environment variables:
- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
- `OLLAMA_CHAT_MODEL` (default: `mistral`)
- `OLLAMA_EMBED_MODEL` (default: `nomic-embed-text`)

## How It Works

### Indexing Phase:
```
PDF/DOCX → Docling → Markdown → Ollama Embeddings → ChromaDB
```

### Query Phase:
```
Question → Ollama Embeddings → ChromaDB Search → Retrieve Context → Mistral → Answer
```

## Key Files

| File | Purpose |
|------|---------|
| `embed_documents.py` | Batch process all documents |
| `app.py` | Streamlit web interface |
| `ollama_client.py` | Ollama API wrapper |
| `rag_retriever.py` | Query & answer generation |
| `rag_config.py` | Configuration |
| `ingest.py` | Document ingestion (used by app.py) |

## Why No LangChain?

This implementation uses direct API calls for simplicity:
- Fewer dependencies
- More control
- Faster execution
- ~50 lines vs 200+ with LangChain

## Troubleshooting

**Connection Error:**
- Ensure Ollama is running

**Model Not Found:**
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

**Wrong Answers:**
- Re-embed documents: `python embed_documents.py`

## Features

- ✅ 100% offline/local
- ✅ No API keys needed
- ✅ Privacy-focused
- ✅ Supports PDF & DOCX
- ✅ Semantic search
- ✅ Context-aware answers
