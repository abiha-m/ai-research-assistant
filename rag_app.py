# rag_app.py
# Streamlit web interface for RAG question answering

import streamlit as st
from qa_engine import QAEngine
from rag_pipeline import process_pdf_and_store
import os

st.set_page_config(page_title="AI Research Assistant", layout="wide")

st.title("📚 AI Research Assistant")
st.markdown("Ask questions about your documents. Upload a PDF and get answers.")

# Initialize session state
if "engine" not in st.session_state:
    st.session_state.engine = QAEngine("research_docs")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for PDF upload
with st.sidebar:
    st.header("Document Management")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        # Save uploaded file
        file_path = f"uploaded_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                result = process_pdf_and_store(file_path)
                if result.get("error"):
                    st.error(f"Error: {result['error']}")
                else:
                    st.success(f"Processed {result['pages']} pages, {result['total_chunks']} chunks")
                    st.session_state.engine = QAEngine("research_docs")
                    st.session_state.messages = []

    st.divider()

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared.")

    if st.button("Clear Document Collection"):
        st.session_state.engine.manager.clear_collection()
        st.success("Collection cleared.")

    stats = st.session_state.engine.manager.get_collection_stats()
    st.divider()
    st.caption(f"Documents in collection: {stats.get('document_count', 0)}")

# Main chat interface
st.subheader("Chat with your documents")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.engine.ask(prompt, include_sources=True)
            response = result["answer"]

            # Show sources if available
            if result.get("sources"):
                response += "\n\n**Sources:**"
                for i, source in enumerate(result["sources"][:3]):
                    response += f"\n{i+1}. {source['text']}"

            st.markdown(response)

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})