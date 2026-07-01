# embeddings_manager.py
# Generate and store embeddings for RAG

import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmbeddingsManager:
    """
    Manage embeddings and vector storage for RAG.
    """

    def __init__(self, collection_name="research_docs"):
        """
        Initialize the embeddings manager.

        Parameters:
            collection_name (str): Name of the Chroma collection
        """
        # Initialize Chroma client (persistent storage)
        self.client = chromadb.PersistentClient(path="./chroma_db")

        # Set up OpenAI embeddings
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-ada-002"
        )

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Using existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            print(f"Created new collection: {collection_name}")

    def add_chunks(self, chunks, chunk_ids=None, metadatas=None):
        """
        Add text chunks to the vector database.

        Parameters:
            chunks (list): List of text strings or dicts with 'text' key
            chunk_ids (list): Optional list of IDs for the chunks
            metadatas (list): Optional list of metadata dicts for each chunk

        Returns:
            int: Number of chunks added
        """
        if not chunks:
            print("No chunks to add.")
            return 0

        # Extract text from chunks
        texts = []
        ids = []
        metadata_list = []

        for i, chunk in enumerate(chunks):
            if isinstance(chunk, dict):
                text = chunk.get("text", "")
                # Use provided metadata or extract from chunk
                if metadatas and i < len(metadatas):
                    metadata = metadatas[i]
                else:
                    metadata = {k: v for k, v in chunk.items() if k != "text"}
            else:
                text = chunk
                # Use provided metadata or create default
                if metadatas and i < len(metadatas):
                    metadata = metadatas[i]
                else:
                    metadata = {"source": "unknown", "chunk_id": i}

            if text and len(text.strip()) > 0:
                texts.append(text)
                # Generate ID if not provided
                if chunk_ids and i < len(chunk_ids):
                    ids.append(chunk_ids[i])
                else:
                    ids.append(f"chunk_{i}")
                
                # Ensure metadata is a non-empty dict
                if not metadata:
                    metadata = {"source": "unknown", "chunk_id": i}
                metadata_list.append(metadata)

        if not texts:
            print("No valid text chunks found.")
            return 0

        # Add to Chroma collection
        try:
            self.collection.add(
                documents=texts,
                ids=ids,
                metadatas=metadata_list
            )
            print(f"Added {len(texts)} chunks to vector database.")
            return len(texts)
        except Exception as e:
            print(f"Error adding chunks: {str(e)}")
            return 0

    def add_chunks_from_pdf(self, pdf_path, chunk_size=500, chunk_overlap=50):
        """
        Load a PDF, split into chunks, and add to vector database.

        Parameters:
            pdf_path (str): Path to the PDF file
            chunk_size (int): Size of each chunk in characters
            chunk_overlap (int): Overlap between chunks

        Returns:
            int: Number of chunks added
        """
        try:
            # Import here to avoid circular imports
            from pdf_processor import extract_text_from_pdf, split_text_into_chunks
            
            # Extract text from PDF
            text = extract_text_from_pdf(pdf_path)
            if not text:
                print(f"Failed to extract text from {pdf_path}")
                return 0
            
            # Split into chunks
            chunks = split_text_into_chunks(text, chunk_size, chunk_overlap)
            if not chunks:
                print("No chunks created from PDF.")
                return 0
            
            # Create metadata for each chunk
            metadatas = []
            for i, chunk in enumerate(chunks):
                metadatas.append({
                    "source": os.path.basename(pdf_path),
                    "chunk_id": i,
                    "chunk_size": len(chunk)
                })
            
            # Add to vector database
            return self.add_chunks(chunks, metadatas=metadatas)
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return 0

    def search(self, query, n_results=5):
        """
        Search for similar chunks in the vector database.

        Parameters:
            query (str): The search query
            n_results (int): Number of results to return

        Returns:
            list: List of matching chunks with metadata
        """
        if not query or len(query.strip()) == 0:
            print("Empty query provided.")
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            # Format results
            formatted_results = []
            if results and results.get("documents") and len(results["documents"]) > 0:
                for i in range(len(results["documents"][0])):
                    result = {
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") and len(results["metadatas"]) > 0 else {},
                        "score": results["distances"][0][i] if results.get("distances") and len(results["distances"]) > 0 else None
                    }
                    formatted_results.append(result)

            print(f"Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results

        except Exception as e:
            print(f"Error searching: {str(e)}")
            return []

    def get_collection_stats(self):
        """
        Get statistics about the collection.

        Returns:
            dict: Collection statistics
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection.name,
                "document_count": count
            }
        except Exception as e:
            print(f"Error getting stats: {str(e)}")
            return {}

    def clear_collection(self):
        """
        Clear all documents from the collection.
        """
        try:
            all_ids = self.collection.get()["ids"]
            if all_ids:
                self.collection.delete(ids=all_ids)
                print("Collection cleared.")
            else:
                print("Collection is already empty.")
        except Exception as e:
            print(f"Error clearing collection: {str(e)}")

    def delete_collection(self):
        """
        Delete the entire collection.
        """
        try:
            self.client.delete_collection(self.collection.name)
            print(f"Collection '{self.collection.name}' deleted.")
        except Exception as e:
            print(f"Error deleting collection: {str(e)}")


if __name__ == "__main__":
    # Test the embeddings manager
    print("="*50)
    print("TESTING EMBEDDINGS MANAGER")
    print("="*50)

    # Initialize
    manager = EmbeddingsManager("test_collection")

    # Test chunks
    test_chunks = [
        "Artificial intelligence is the simulation of human intelligence processes by machines.",
        "Machine learning is a subset of AI that focuses on data-driven learning.",
        "Deep learning uses neural networks with many layers to learn from data.",
        "Natural language processing enables machines to understand human language.",
        "Computer vision allows machines to interpret and understand visual information."
    ]

    # Add chunks with metadata
    print("\nAdding test chunks...")
    metadatas = [
        {"source": "test_data", "topic": "AI"},
        {"source": "test_data", "topic": "ML"},
        {"source": "test_data", "topic": "Deep Learning"},
        {"source": "test_data", "topic": "NLP"},
        {"source": "test_data", "topic": "Computer Vision"}
    ]
    manager.add_chunks(test_chunks, chunk_ids=[f"test_{i}" for i in range(len(test_chunks))], metadatas=metadatas)

    # Get stats
    print("\nCollection stats:")
    print(manager.get_collection_stats())

    # Search
    print("\nSearching for 'machine learning':")
    results = manager.search("machine learning", n_results=3)
    for i, result in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"  Text: {result['text']}")
        print(f"  Score: {result['score']}")
        print(f"  Metadata: {result['metadata']}")

    # Search again
    print("\nSearching for 'computer vision':")
    results = manager.search("computer vision", n_results=2)
    for i, result in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"  Text: {result['text']}")
        print(f"  Score: {result['score']}")
        print(f"  Metadata: {result['metadata']}")

    print("\nTest complete!")