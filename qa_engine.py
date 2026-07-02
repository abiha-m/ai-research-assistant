# qa_engine.py
# Question answering using RAG with GPT

import os
from openai import OpenAI
from dotenv import load_dotenv
from embeddings_manager import EmbeddingsManager

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

class QAEngine:
    """
    Question-answering engine using RAG.
    Retrieves relevant chunks and generates answers with GPT.
    """

    def __init__(self, collection_name="research_docs"):
        """
        Initialize the QA engine.

        Parameters:
            collection_name (str): Name of the Chroma collection
        """
        self.manager = EmbeddingsManager(collection_name)
        self.conversation_history = []

    def retrieve_context(self, query, n_results=5):
        """
        Retrieve relevant chunks for a query.

        Parameters:
            query (str): The question
            n_results (int): Number of chunks to retrieve

        Returns:
            list: Retrieved chunks with metadata
        """
        return self.manager.search(query, n_results)

    def generate_answer(self, query, context_chunks, max_tokens=300):
        """
        Generate an answer using GPT with retrieved context.

        Parameters:
            query (str): The question
            context_chunks (list): List of retrieved chunks
            max_tokens (int): Maximum length of the answer

        Returns:
            str: Generated answer
        """
        if not context_chunks:
            return "I don't have enough information to answer that question."

        # Build context from retrieved chunks
        context_text = "\n\n".join([chunk["text"] for chunk in context_chunks])

        # Create system prompt
        system_prompt = """You are a helpful AI assistant that answers questions based on the provided context.
        Only use information from the context to answer the question.
        If the context does not contain the answer, say so clearly.
        Be concise but thorough in your response."""

        # Create user prompt
        user_prompt = f"""Context:
{context_text}

Question: {query}

Answer based only on the context above:"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating answer: {str(e)}"

    def ask(self, query, n_results=5, include_sources=False):
        """
        Ask a question and get an answer.

        Parameters:
            query (str): The question
            n_results (int): Number of chunks to retrieve
            include_sources (bool): Whether to include sources in response

        Returns:
            dict: Answer with optional sources
        """
        # Retrieve relevant chunks
        chunks = self.retrieve_context(query, n_results)

        # Generate answer
        answer = self.generate_answer(query, chunks)

        # Store conversation history
        self.conversation_history.append({
            "question": query,
            "answer": answer
        })

        result = {"answer": answer}

        if include_sources:
            result["sources"] = [
                {"text": chunk["text"][:200] + "...", "score": chunk.get("score")}
                for chunk in chunks[:3]
            ]

        return result

    def chat(self):
        """
        Interactive chat session with the QA engine.
        """
        print("\n" + "="*50)
        print("AI RESEARCH ASSISTANT")
        print("Ask questions about your documents.")
        print("Type 'exit' or 'quit' to end.")
        print("="*50)

        while True:
            query = input("\nQuestion: ").strip()

            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break

            if not query:
                continue

            print("\nThinking...")
            result = self.ask(query, include_sources=True)

            print("\nAnswer:")
            print("-"*50)
            print(result["answer"])
            print("-"*50)

            if result.get("sources"):
                print("\nSources:")
                for i, source in enumerate(result["sources"]):
                    print(f"{i+1}. {source['text']}")
                    if source.get("score"):
                        print(f"   (relevance: {source['score']:.3f})")

            print("\n" + "-"*50)

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.")

    def get_history(self):
        """Get conversation history."""
        return self.conversation_history

if __name__ == "__main__":
    import sys

    print("="*50)
    print("QA ENGINE TEST")
    print("="*50)

    # Initialize QA engine
    engine = QAEngine("research_docs")

    # Check if collection has documents
    stats = engine.manager.get_collection_stats()
    if stats.get("document_count", 0) == 0:
        print("\nWarning: No documents found in the collection.")
        print("Please run rag_pipeline.py first to load a PDF.")
        print("\nContinue anyway? (y/n)")
        choice = input().lower()
        if choice != 'y':
            sys.exit(1)

    # Test questions
    test_questions = [
        "What is the main topic of this document?",
        "Summarize the key points.",
        "What does the author argue?",
    ]

    print("\nRunning test questions...")
    for q in test_questions:
        print(f"\nQ: {q}")
        result = engine.ask(q, include_sources=True)
        print(f"A: {result['answer']}")
        print("-"*30)

    # Start interactive chat
    print("\nStarting interactive chat session...")
    engine.chat()