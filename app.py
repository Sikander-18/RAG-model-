import os
from pathlib import Path

import streamlit as st

from ingest import ingest_file, ensure_dirs
from rag_retriever import generate_answer
from rag_config import paths


def main():
    st.set_page_config(page_title="Local RAG with Mistral (Ollama)", layout="wide")
    st.title("📚 Local RAG with Mistral 7B (Ollama)")
    st.markdown(
        "Fully offline RAG using **Docling** for parsing, **ChromaDB** for retrieval, "
        "and **Mistral 7B** served via **Ollama**."
    )

    ensure_dirs()

    with st.sidebar:
        st.header("📄 Document Upload")
        uploaded_file = st.file_uploader(
            "Upload PDF or DOCX",
            type=["pdf", "docx"],
        )
        if uploaded_file is not None:
            save_path = Path(paths.data_dir) / uploaded_file.name
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Ingesting document..."):
                try:
                    added = ingest_file(str(save_path))
                    st.success(f"Ingested {added} document(s) from {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Failed to ingest: {e}")

        st.markdown("---")
        st.caption(
            f"Data dir: `{paths.data_dir}`  \n"
            f"Markdown dir: `{paths.markdown_dir}`  \n"
            f"Chroma dir: `{paths.chroma_dir}`"
        )

    st.header("🔎 Ask a question about your documents")
    query = st.text_input("Your question", placeholder="e.g. Summarize the key points of the uploaded document.")
    top_k = st.slider("Number of context chunks", min_value=1, max_value=8, value=4)

    if st.button("Generate Answer") and query.strip():
        with st.spinner("Thinking with Mistral via Ollama..."):
            try:
                answer, metadatas = generate_answer(query, k=top_k)
                st.subheader("🧠 Answer")
                st.write(answer)

                if metadatas:
                    st.subheader("📚 Sources")
                    # Get unique sources
                    unique_sources = list(set(meta.get('source', 'unknown') for meta in metadatas))
                    for i, source in enumerate(unique_sources, start=1):
                        st.markdown(f"**Source {i}**: `{source}`")
            except Exception as e:
                st.error(f"Error generating answer: {e}")


if __name__ == "__main__":
    main()


