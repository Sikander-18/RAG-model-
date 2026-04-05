# 🔍 Local RAG IDE Assistant

A professional, privacy-first, and fully offline Retrieval-Augmented Generation (RAG) assistant. This project transforms your local documents (PDF, DOCX) into an interactive AI knowledge base with a modern, VS Code-inspired interface.

---

## ✨ Features

- **Modern Chat Interface**: ChatGPT-style message bubbles with distinct user/AI alignment.
- **IDE Layout**: Integrated Activity Bar, Sidebar (Explorer/Search), and Terminal Panel for real-time logs.
- **Deep Document Retrieval**: Optimized search depth (k=12) ensures the AI synthesizes information across multiple documents.
- **High-Performance Parsing**: Powered by **Docling** for accurate PDF and DOCX conversion.
- **Local AI Power**: Runs completely on your hardware via **Ollama** (supports Mistral, Llama, etc.).
- **Privacy First**: No data leaves your machine. No API keys required.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | React, Vite, TypeScript, Lucide Icons |
| **Backend** | FastAPI, Python 3.10+ |
| **Document Parsing** | IBM Docling |
| **Vector Database** | ChromaDB |
| **LLM Engine** | Ollama (Mistral / Nomic-Embed-Text) |

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Node.js** (v18+)
- **[Ollama](https://ollama.com)** installed and running.

### 2. AI Model Setup
Pull the required models for chat and embeddings:
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### 3. Backend Setup
```bash
# Navigate to root
cd RAG-model-

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 4. Frontend Setup
```bash
# Navigate to frontend
cd frontend
npm install
```

---

## 📖 How to Run

### Step 1: Start the Backend
From the root directory (with venv activated):
```bash
python backend/api.py
```
*Backend runs on `http://localhost:8080`*

### Step 2: Start the Frontend
From the `frontend` directory:
```bash
npm run dev
```
*App accessible at `http://localhost:5173`*

---

## 📂 Project Structure

```text
RAG-model-/
├── backend/            # FastAPI & AI Logic
│   ├── api.py          # WebSocket/REST Endpoints
│   ├── ingest.py       # Document Processing
│   └── rag_retriever.py # AI Generation & Context Search
├── frontend/           # React + Vite Application
│   ├── src/components/ # UI Modules (Chat, Sidebar, Terminal)
│   └── App.tsx         # Main Layout Logic
└── documents/          # Private Data (Git Ignored)
    ├── raw_documents/  # Place your PDFs here
    └── vector_data/    # ChromaDB database
```

---

## 🛡️ License & Privacy
This software is provided as-is for local use. No telemetry or external calls are made to third-party AI providers.
