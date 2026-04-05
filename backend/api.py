import os
import shutil
import asyncio
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ingest import ingest_file, ensure_dirs, delete_from_chroma
from rag_retriever import generate_answer, generate_answer_stream
from rag_config import paths

app = FastAPI(title="RAG Backend API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist on startup
ensure_dirs()

# --- Connection Manager for WebSockets ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def disappearance(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

async def log_to_frontend(message: str, type: str = "info"):
    prefix = "[INFO]" if type == "info" else "[SUCCESS]" if type == "success" else "[ERROR]"
    full_msg = f"{prefix} {message}"
    await manager.broadcast(full_msg)

# --- Routes ---

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/")
async def root():
    return {"status": "online", "model": "Mistral-7B"}

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await manager.disappearance(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/query")
async def query_rag(request: QueryRequest):
    """Generate an answer from documents based on the query with streaming."""
    try:
        await log_to_frontend(f"Processing query: '{request.query}'...")
        
        # We use StreamingResponse to send tokens one by one
        return StreamingResponse(
            generate_answer_stream(request.query),
            media_type="text/plain"
        )
    except Exception as e:
        await log_to_frontend(f"Query error: {str(e)}", "error")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to raw_documents and trigger ingestion."""
    try:
        save_path = Path(paths.raw_dir) / file.filename
        await log_to_frontend(f"Uploading {file.filename}...")
        
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        await log_to_frontend(f"File saved. Starting conversion and indexing...")
        
        # Ingest the file into ChromaDB
        # Note: ingest_file is synchronous, so we'll run it and log after
        chunks_added = ingest_file(str(save_path))
        
        await log_to_frontend(f"Ingestion complete. {chunks_added} chunks added to vector database.", "success")
        
        return {
            "filename": file.filename, 
            "status": "success", 
            "chunks_added": chunks_added
        }
    except Exception as e:
        await log_to_frontend(f"Upload error: {str(e)}", "error")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def list_files():
    """List all documents in the raw_documents directory."""
    raw_path = Path(paths.raw_dir)
    files = [f.name for f in raw_path.glob("*") if f.is_file() and not f.name.startswith(".")]
    return {"files": files}

@app.delete("/files/{filename}")
async def delete_file(filename: str):
    """Delete a document and its processed version + cleanup vector DB."""
    try:
        raw_file = Path(paths.raw_dir) / filename
        processed_file = Path(paths.processed_dir) / f"{raw_file.stem}.md"
        
        await log_to_frontend(f"Deleting {filename} from storage and vector database...")
        
        if raw_file.exists():
            os.remove(raw_file)
        if processed_file.exists():
            os.remove(processed_file)
            
        # Cleanup ChromaDB
        delete_from_chroma(filename)
        
        await log_to_frontend(f"Deletion of {filename} completed.", "success")
        return {"status": "deleted", "filename": filename}
    except Exception as e:
        await log_to_frontend(f"Deletion error: {str(e)}", "error")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
