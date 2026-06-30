# demo.py
# Quick demonstration of the summarizer

from summarizer import summarize, read_file, save_summary

print("="*60)
print("TEXT SUMMARIZER DEMO")
print("="*60)

# Demo 1: Summarize a sample text
sample_text = """
Artificial intelligence (AI) is the simulation of human intelligence processes by machines, 
especially computer systems. These processes include learning, reasoning, and self-correction. 
Specific applications of AI include expert systems, natural language processing (NLP), 
speech recognition, and machine vision. AI research has been highly successful in developing 
effective techniques for solving a wide range of problems, from game playing to medical diagnosis.
"""

print("\nDemo 1: Summarizing sample text")
print("-"*60)
print("Original text:", sample_text[:100], "...")
summary = summarize(sample_text, max_length=30)
print("Summary:", summary)

# Demo 2: Using a file (if it exists)
print("\n" + "="*60)
print("Demo 2: Summarizing from file")
print("-"*60)

try:
    content = read_file("sample_input.txt")
    if not content.startswith("Error"):
        summary = summarize(content, max_length=50)
        print("Summary generated from file.")
        print("Summary:", summary[:200] + ("..." if len(summary) > 200 else ""))
    else:
        print("No sample file found. Create sample_input.txt to test.")
except Exception as e:
    print(f"Error in Demo 2: {str(e)}")

print("\n" + "="*60)
print("Demo complete! Check summary_log.txt for detailed logs.")
print("="*60)