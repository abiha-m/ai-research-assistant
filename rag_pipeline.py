# rag_pipeline.py
# Full RAG pipeline with multi-PDF support

import os
from pdf_processor import load_pdf, split_documents_into_chunks
from embeddings_manager import EmbeddingsManager

def process_pdf_and_store(pdf_path, collection_name="research_docs"):
    """
    Process a single PDF and store in vector DB.

    Parameters:
        pdf_path (str): Path to the PDF file
        collection_name (str): Name of the Chroma collection

    Returns:
        dict: Results summary
    """
    print(f"Processing: {os.path.basename(pdf_path)}")

    # Load PDF
    documents = load_pdf(pdf_path)
    if documents is None:
        return {"error": f"Failed to load {pdf_path}"}

    total_pages = len(documents)

    # Split into chunks
    chunks = split_documents_into_chunks(documents, chunk_size=500, chunk_overlap=50)

    # Add source info to each chunk
    for chunk in chunks:
        chunk["source"] = os.path.basename(pdf_path)

    # Store chunks
    manager = EmbeddingsManager(collection_name)

    chunk_texts = []
    chunk_ids = []
    chunk_metadatas = []

    for i, chunk in enumerate(chunks):
        chunk_texts.append(chunk["text"])
        chunk_ids.append(f"doc_{i}")
        chunk_metadatas.append({
            "source": chunk.get("source", "unknown"),
            "page": chunk.get("page", 0)
        })

    manager.add_chunks(chunk_texts, chunk_ids, chunk_metadatas)

    stats = manager.get_collection_stats()

    return {
        "pages": total_pages,
        "total_chunks": len(chunks),
        "collection": stats
    }


def process_multiple_pdfs(pdf_paths, collection_name="research_docs"):
    """
    Process multiple PDFs and store in vector DB.

    Parameters:
        pdf_paths (list): List of PDF file paths
        collection_name (str): Name of the Chroma collection

    Returns:
        dict: Results summary
    """
    print("="*50)
    print("PROCESSING MULTIPLE PDFS")
    print("="*50)

    manager = EmbeddingsManager(collection_name)
    all_chunks = []
    total_pages = 0
    processed_pdfs = 0

    for pdf_path in pdf_paths:
        print(f"\nProcessing: {os.path.basename(pdf_path)}")

        # Load PDF
        documents = load_pdf(pdf_path)
        if documents is None:
            print(f"  Skipping {pdf_path} - failed to load")
            continue

        processed_pdfs += 1
        total_pages += len(documents)

        # Split into chunks
        chunks = split_documents_into_chunks(documents, chunk_size=500, chunk_overlap=50)

        # Add source info to each chunk
        for chunk in chunks:
            chunk["source"] = os.path.basename(pdf_path)

        all_chunks.extend(chunks)

        print(f"  Added {len(chunks)} chunks from {len(documents)} pages")

    if not all_chunks:
        return {"error": "No chunks created from any PDF"}

    # Store all chunks
    chunk_texts = []
    chunk_ids = []
    chunk_metadatas = []

    for i, chunk in enumerate(all_chunks):
        chunk_texts.append(chunk["text"])
        chunk_ids.append(f"doc_{i}")
        chunk_metadatas.append({
            "source": chunk.get("source", "unknown"),
            "page": chunk.get("page", 0)
        })

    manager.add_chunks(chunk_texts, chunk_ids, chunk_metadatas)

    stats = manager.get_collection_stats()

    return {
        "pdfs_processed": processed_pdfs,
        "total_pages": total_pages,
        "total_chunks": len(all_chunks),
        "collection": stats
    }


def query_pdf(query, n_results=5, collection_name="research_docs"):
    """
    Query the vector database for relevant chunks.

    Parameters:
        query (str): The search query
        n_results (int): Number of results to return
        collection_name (str): Name of the Chroma collection

    Returns:
        list: List of matching chunks
    """
    try:
        manager = EmbeddingsManager(collection_name)
        results = manager.search(query, n_results)
        return results
    except Exception as e:
        print(f"Error querying: {str(e)}")
        return []


if __name__ == "__main__":
    import sys

    print("RAG PIPELINE TEST")
    print("="*50)

    # Get PDF path
    pdf_path = input("Enter path to PDF file: ").strip()
    if not pdf_path:
        print("No PDF path provided.")
        sys.exit(1)

    # Process the PDF
    result = process_pdf_and_store(pdf_path)

    if result.get("error"):
        print(f"Error: {result['error']}")
        sys.exit(1)

    print("\n" + "="*50)
    print("PROCESSING COMPLETE")
    print("="*50)
    print(f"Pages processed: {result['pages']}")
    print(f"Total chunks: {result['total_chunks']}")
    print(f"Collection stats: {result['collection']}")

    # Test query
    print("\n" + "="*50)
    print("TEST QUERY")
    print("="*50)
    query = input("\nEnter a question about your document: ").strip()

    if query:
        results = query_pdf(query)
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results):
            print(f"\nResult {i+1} (Score: {result['score']}):")
            print(f"  {result['text'][:300]}...")
            