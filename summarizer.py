# summarizer.py - Complete summarizer with all functions
# This script contains all the core functions used by app.py

import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def read_file(file_path):
    """
    Read text from a file.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        str: Content of the file or error message
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def save_summary(summary, output_path):
    """
    Save summary to a file.
    
    Args:
        summary (str): The summary text
        output_path (str): Path to save the summary
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(summary)
        return True
    except Exception as e:
        print(f"Error saving summary: {str(e)}")
        return False

def log_summary(input_text, output_text):
    """
    Log the input and output to a file.
    
    Args:
        input_text (str): The original text
        output_text (str): The summary
    """
    try:
        with open("summary_log.txt", "a", encoding='utf-8') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"\n--- {timestamp} ---\n")
            log_file.write(f"Input: {input_text[:200]}...\n")
            log_file.write(f"Output: {output_text}\n")
    except Exception as e:
        print(f"Warning: Could not write to log: {str(e)}")

def summarize(text, max_length=100):
    """
    Summarize the given text using OpenAI's GPT model.
    
    Args:
        text (str): The text to summarize
        max_length (int): Maximum length of the summary in words
    
    Returns:
        str: The summarized text or error message
    """
    if not text or len(text.strip()) == 0:
        return "Error: No text provided."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that summarizes text concisely in {max_length} words or less."},
                {"role": "user", "content": f"Summarize this: {text}"}
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        summary = response.choices[0].message.content
        
        if not summary:
            return "Error: Received empty response from the API."
        
        # Log the summary
        log_summary(text, summary)
        
        return summary
        
    except Exception as e:
        return f"Error: {str(e)}"

# For testing when run directly
if __name__ == "__main__":
    print("Testing summarizer functions...")
    
    # Test read_file
    test_content = read_file("sample_input.txt")
    if test_content.startswith("Error"):
        print("No sample file found. Creating one...")
        with open("sample_input.txt", "w", encoding='utf-8') as f:
            f.write("This is a sample text file for testing the summarizer.\n\nPython is a programming language that lets you work quickly and integrate systems more effectively.")
    
    # Test summarize
    test_text = "Python is a programming language that lets you work quickly and integrate systems more effectively."
    summary = summarize(test_text, max_length=20)
    print(f"Test summary: {summary}")
    