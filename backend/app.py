import os
from pathlib import Path

import streamlit as st

from ingest import ingest_file, ensure_dirs
from rag_retriever import generate_answer
from rag_config import paths


def main():
    st.set_page_config(page_title="Local RAG Assistant", page_icon="📚", layout="wide")
    
    st.title("📚 Local RAG Assistant")
    st.markdown(
        "Fully offline RAG system using **Docling** for document parsing, **ChromaDB** for vector storage, "
        "and **Mistral 7B** via **Ollama** for intelligence."
    )

    # Ensure all directories exist on startup
    ensure_dirs()

    with st.sidebar:
        st.header("📄 Document Management")
        uploaded_file = st.file_uploader(
            "Upload a document to add to the knowledge base",
            type=["pdf", "docx"],
        )
        
        if uploaded_file is not None:
            save_path = Path(paths.raw_dir) / uploaded_file.name
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner(f"Ingesting {uploaded_file.name}..."):
                try:
                    chunks_added = ingest_file(str(save_path))
                    st.success(f"Successfully added {chunks_added} chunks from '{uploaded_file.name}'")
                except Exception as e:
                    st.error(f"❌ Failed to process document: {type(e).__name__}")
                    st.exception(e)  # This shows the full traceback to help diagnostic

        st.markdown("---")
        st.subheader("⚙️ System Info")
        st.caption(f"**Knowledge Base**: `{paths.raw_dir}`")
        st.caption(f"**Vector Database**: `{paths.vector_db_dir}`")
        
        if st.button("Refresh Index"):
            from ingest import ingest_folder
            with st.spinner("Re-indexing all documents..."):
                total_chunks = ingest_folder()
                st.info(f"Re-indexed {total_chunks} total chunks.")

    st.divider()

    st.header("🔎 Ask your data")
    query = st.text_input(
        "Enter your question:", 
        placeholder="e.g., What are the main findings in the uploaded document?",
        key="query_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        top_k = st.slider("Context chunks (k)", min_value=1, max_value=10, value=4)
    
    if st.button("Ask Assistant", type="primary") and query.strip():
        with st.spinner("Analyzing documents..."):
            try:
                answer, metadatas = generate_answer(query, k=top_k)
                
                st.markdown("### 🧠 Assistant Response")
                st.write(answer)

                if metadatas:
                    with st.expander("📚 View Sources & Context"):
                        # Get unique sources
                        unique_sources = sorted(list(set(meta.get('source', 'unknown') for meta in metadatas)))
                        for i, source in enumerate(unique_sources, start=1):
                            st.markdown(f"**Source {i}**: `{source}`")
                        
                        st.markdown("---")
                        st.markdown("**Retrieved Chunks:**")
                        for idx, meta in enumerate(metadatas):
                            st.info(f"Chunk {idx+1} from `{meta.get('source', 'unknown')}`")
            except Exception as e:
                st.error(f"An error occurred while generating the answer: {e}")


if __name__ == "__main__":
    main()
