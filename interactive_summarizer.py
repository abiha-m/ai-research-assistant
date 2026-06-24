# interactive_summarizer.py
# Simple interactive summarizer with logging

import os
import datetime  # NEW: For logging timestamps
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def summarize(text, max_length=100):
    if not text or len(text.strip()) == 0:
        return "Error: No text provided."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Summarize the following text in about {max_length} words:\n\n{text}"}
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        summary = response.choices[0].message.content
        
        # NEW: Log the input and output to a file
        with open("summary_log.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"\n--- {timestamp} ---\n")
            log_file.write(f"Input: {text[:200]}...\n")
            log_file.write(f"Output: {summary}\n")
        
        return summary
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Text Summarizer")
    print("Enter your text below. Press Ctrl+D (or Ctrl+Z on Windows) when done.")
    print("To exit, type 'quit'.")
    
    while True:
        print("\nEnter text (or 'quit' to exit):")
        user_input = input()
        if user_input.lower() == 'quit':
            break
        if user_input:
            summary = summarize(user_input)
            print(f"\nSummary: {summary}")