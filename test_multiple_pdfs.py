# test_multiple_pdfs.py
# Test processing multiple PDFs

from rag_pipeline import process_multiple_pdfs
import os

# Find all PDFs in the current directory
pdf_files = [f for f in os.listdir(".") if f.endswith(".pdf")]

if not pdf_files:
    print("No PDF files found in current directory.")
    print("Please add some PDFs to test.")
else:
    print(f"Found {len(pdf_files)} PDF files:")
    for f in pdf_files:
        print(f"  - {f}")

    result = process_multiple_pdfs(pdf_files)

    if result.get("error"):
        print(f"Error: {result['error']}")
    else:
        print("\nProcessing complete!")
        print(f"PDFs processed: {result['pdfs_processed']}")
        print(f"Total pages: {result['total_pages']}")
        print(f"Total chunks: {result['total_chunks']}")