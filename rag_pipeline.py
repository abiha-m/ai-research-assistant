# rag_pipeline.py
# Full RAG pipeline: PDF → chunks → embeddings → search

from pdf_processor import load_pdf, split_documents_into_chunks
from embeddings_manager import EmbeddingsManager

def process_pdf_and_store(pdf_path, collection_name="research_docs"):
    """
    Full pipeline: load PDF, split into chunks, and store in vector DB.

    Parameters:
        pdf_path (str): Path to the PDF file
        collection_name (str): Name of the Chroma collection

    Returns:
        dict: Results of the processing
    """
    print("="*50)
    print("PROCESSING PDF FOR RAG")
    print("="*50)

    # Step 1: Load PDF
    print("\nStep 1: Loading PDF...")
    documents = load_pdf(pdf_path)
    if documents is None:
        return {"error": "Failed to load PDF"}

    # Step 2: Split into chunks
    print("\nStep 2: Splitting into chunks...")
    chunks = split_documents_into_chunks(documents, chunk_size=500, chunk_overlap=50)

    if not chunks:
        return {"error": "No chunks created"}

    # Step 3: Store in vector database
    print("\nStep 3: Storing in vector database...")
    manager = EmbeddingsManager(collection_name)

    # Prepare chunks for storage
    chunk_texts = []
    chunk_ids = []
    for i, chunk in enumerate(chunks):
        chunk_texts.append(chunk["text"])
        chunk_ids.append(f"{pdf_path.replace('/', '_')}_{i}")

    manager.add_chunks(chunk_texts, chunk_ids)

    # Step 4: Get stats
    stats = manager.get_collection_stats()

    return {
        "pages": len(documents),
        "total_chunks": len(chunks),
        "collection": stats
    }

def query_pdf(query, collection_name="research_docs", n_results=5):
    """
    Query the vector database for information.

    Parameters:
        query (str): The question or search query
        collection_name (str): Name of the collection
        n_results (int): Number of results to return

    Returns:
        list: Search results
    """
    manager = EmbeddingsManager(collection_name)
    return manager.search(query, n_results)

if __name__ == "__main__":
    import sys

    print("RAG PIPELINE TEST")
    print("="*50)

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