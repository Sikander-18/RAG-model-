# Local RAG Assistant Assistant (Docling + ChromaDB + Ollama)

## 🚀 Overview

A fully offline, privacy-first Retrieval-Augmented Generation (RAG) system.
- **Docling**: High-performance document parsing (PDF/DOCX).
- **ChromaDB**: Reliable vector storage for context retrieval.
- **Ollama**: Local AI power (Mistral for chat, Nomic for embeddings).
- **Streamlit**: Clean, intuitive web interface.

## 🛠️ Prerequisites

1.  **Python 3.10+**
2.  **[Ollama](https://ollama.com)** installed and running.
3.  **Pull Required Models**:
    ```bash
    ollama pull mistral
    ollama pull nomic-embed-text
    ```

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 📂 Project Structure

```
documents/
├── raw_documents/       ← Place original PDF/DOCX here
├── processed_documents/ ← Converted markdown files
└── vector_data/         ← ChromaDB database files
```

## 📖 Usage

### 🚀 Launch the Web App
The simplest way to use the system is through the Streamlit interface:
```bash
streamlit run app.py
```
1.  **Upload**: Click the sidebar to upload documents. They are automatically parsed, chunked, and indexed.
2.  **Chat**: Ask questions in the main area to get answers based on your documents.

### 📥 Batch Ingestion (Optional)
To index a folder of documents manually:
```bash
python ingest.py
```

## ⚙️ Configuration
Edit `rag_config.py` to change:
- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
- `chat_model` (default: `mistral`)
- `embed_model` (default: `nomic-embed-text`)

## 🛡️ Privacy & Offline Use
This system is designed to be **100% local**. No data ever leaves your machine. No API keys or cloud subscriptions are required.
