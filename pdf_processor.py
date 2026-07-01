# pdf_processor.py
# PDF loading, text extraction, and chunking for RAG

import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    """
    Load a PDF file and extract its text content.

    Parameters:
        file_path (str): Path to the PDF file

    Returns:
        list: List of Document objects, or None if error
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from {os.path.basename(file_path)}")
        return documents
    except Exception as e:
        print(f"Error loading PDF: {str(e)}")
        return None

def extract_text_from_pdf(file_path):
    """
    Extract and combine all text from a PDF file.

    Parameters:
        file_path (str): Path to the PDF file

    Returns:
        str: Combined text from all pages, or None if error
    """
    documents = load_pdf(file_path)
    if documents is None:
        return None

    full_text = ""
    for i, doc in enumerate(documents):
        page_text = doc.page_content
        full_text += f"\n--- Page {i+1} ---\n"
        full_text += page_text

    return full_text

def get_pdf_metadata(file_path):
    """
    Extract metadata from a PDF file.

    Parameters:
        file_path (str): Path to the PDF file

    Returns:
        dict: Metadata, or None if error
    """
    documents = load_pdf(file_path)
    if documents is None:
        return None

    # Metadata is usually in the first document
    metadata = documents[0].metadata if documents else {}
    return metadata

def preview_pdf(file_path, num_pages=2):
    """
    Preview the first few pages of a PDF.

    Parameters:
        file_path (str): Path to the PDF file
        num_pages (int): Number of pages to preview

    Returns:
        str: Preview text, or None if error
    """
    documents = load_pdf(file_path)
    if documents is None:
        return None

    preview = ""
    for i in range(min(num_pages, len(documents))):
        page_text = documents[i].page_content
        preview += f"\n--- Page {i+1} Preview ---\n"
        preview += page_text[:500] + ("..." if len(page_text) > 500 else "")
        preview += "\n"

    return preview

def split_text_into_chunks(text, chunk_size=500, chunk_overlap=50):
    """
    Split text into overlapping chunks.

    Parameters:
        text (str): Text to split
        chunk_size (int): Maximum size of each chunk in characters
        chunk_overlap (int): Overlap between chunks in characters

    Returns:
        list: List of text chunks
    """
    if not text or len(text) == 0:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # Try to break at a sentence or word boundary
        if end < text_length:
            # Look for a period, question mark, or exclamation point
            for i in range(end, max(start, end - 50), -1):
                if text[i] in '.!?':
                    end = i + 1
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - chunk_overlap if end < text_length else end

    print(f"Created {len(chunks)} chunks")
    return chunks

def split_documents_into_chunks(documents, chunk_size=500, chunk_overlap=50):
    """
    Split a list of Document objects into text chunks.

    Parameters:
        documents (list): List of Document objects
        chunk_size (int): Maximum size of each chunk in characters
        chunk_overlap (int): Overlap between chunks in characters

    Returns:
        list: List of text chunks with metadata
    """
    chunks = []
    for i, doc in enumerate(documents):
        text = doc.page_content
        page_chunks = split_text_into_chunks(text, chunk_size, chunk_overlap)

        for j, chunk in enumerate(page_chunks):
            chunks.append({
                "text": chunk,
                "page": i + 1,
                "chunk_id": f"page_{i+1}_chunk_{j+1}"
            })

    print(f"Created {len(chunks)} total chunks from {len(documents)} pages")
    return chunks

if __name__ == "__main__":
    # Test the functions
    pdf_path = input("Enter path to PDF file: ").strip()

    if not pdf_path:
        print("No path provided.")
    else:
        print("\n" + "="*50)
        print("TESTING PDF PROCESSOR")
        print("="*50)

        # Test preview
        print("\nPreview:")
        print(preview_pdf(pdf_path, num_pages=2))

        # Test metadata
        print("\nMetadata:")
        print(get_pdf_metadata(pdf_path))

        # Test full extraction
        print("\nExtracting full text...")
        text = extract_text_from_pdf(pdf_path)
        if text:
            print(f"Extracted {len(text)} characters")
            print(f"First 500 characters: {text[:500]}...")
            
            # Test chunking
            print("\n" + "="*50)
            print("TESTING CHUNKING")
            print("="*50)
            chunks = split_text_into_chunks(text, chunk_size=500, chunk_overlap=50)
            print(f"\nFirst 3 chunks:")
            for i, chunk in enumerate(chunks[:3]):
                print(f"\n--- Chunk {i+1} ---")
                print(chunk[:200] + "...")
# Add this test after the existing test code

if __name__ == "__main__":
    # ... existing test code ...

    # Test text splitting
    print("\n" + "="*50)
    print("TESTING TEXT SPLITTER")
    print("="*50)

    test_text = """
    Artificial intelligence is the simulation of human intelligence processes by machines,
    especially computer systems. These processes include learning, reasoning, and self-correction.
    Specific applications of AI include expert systems, natural language processing (NLP),
    speech recognition, and machine vision. AI research has been highly successful in developing
    effective techniques for solving a wide range of problems, from game playing to medical diagnosis.
    """

    chunks = split_text_into_chunks(test_text, chunk_size=100, chunk_overlap=20)
    print(f"\nTest text: {len(test_text)} characters")
    print(f"Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(chunk)
    # Test full workflow: PDF → documents → chunks
    print("\n" + "="*50)
    print("TESTING FULL WORKFLOW")
    print("="*50)

    if pdf_path:
        documents = load_pdf(pdf_path)
        if documents:
            chunks = split_documents_into_chunks(documents, chunk_size=500, chunk_overlap=50)
            print(f"Total chunks created: {len(chunks)}")
            print("\nFirst 2 chunks:")
            for i, chunk in enumerate(chunks[:2]):
                print(f"\nChunk {i+1}: {chunk['text'][:200]}...")
                print(f"  Page: {chunk['page']}")                        