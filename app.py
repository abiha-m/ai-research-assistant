# app.py
# Complete Text Summarizer Application

import os
import sys
from summarizer import read_file, save_summary, summarize, log_summary

def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("          TEXT SUMMARIZER APPLICATION")
    print("="*50)
    print("1. Summarize text from file")
    print("2. Summarize text from clipboard or direct input")
    print("3. Batch summarize all files in folder")
    print("4. View recent logs")
    print("5. Clear logs")
    print("6. Exit")
    print("="*50)
    return input("Enter your choice (1-6): ")

def summarize_from_file():
    """Handle summarizing text from a file."""
    file_path = input("Enter the path to the text file: ").strip()
    
    if not file_path:
        print("No file path provided.")
        return
    
    content = read_file(file_path)
    if content.startswith("Error"):
        print(content)
        return
    
    print(f"\nOriginal content ({len(content)} characters):")
    print("-"*50)
    print(content[:500] + ("..." if len(content) > 500 else ""))
    print("-"*50)
    
    max_length = input("Enter maximum summary length in words (default 100): ").strip()
    max_length = int(max_length) if max_length.isdigit() else 100
    
    print("\nGenerating summary...")
    summary = summarize(content, max_length)
    
    if summary.startswith("Error"):
        print(summary)
        return
    
    print("\nSummary:")
    print("-"*50)
    print(summary)
    print("-"*50)
    
    save_choice = input("\nSave summary to file? (y/n): ").lower()
    if save_choice == 'y':
        output_path = input("Enter output file path (default: output_summary.txt): ").strip()
        if not output_path:
            output_path = "output_summary.txt"
        if save_summary(summary, output_path):
            print(f"Summary saved to {output_path}")

def summarize_direct_input():
    """Handle summarizing text entered directly by the user."""
    print("\nEnter your text below. Press Enter twice when done.")
    print("(Type 'CANCEL' to cancel)")
    
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'CANCEL':
            return
        if line == "" and len(lines) > 0:
            break
        lines.append(line)
    
    content = "\n".join(lines)
    
    if not content or len(content.strip()) == 0:
        print("No text entered.")
        return
    
    max_length = input("Enter maximum summary length in words (default 100): ").strip()
    max_length = int(max_length) if max_length.isdigit() else 100
    
    print("\nGenerating summary...")
    summary = summarize(content, max_length)
    
    if summary.startswith("Error"):
        print(summary)
        return
    
    print("\nSummary:")
    print("-"*50)
    print(summary)
    print("-"*50)

def batch_summarize():
    """Handle batch summarization of all text files in a folder."""
    input_folder = input("Enter the folder path containing text files: ").strip()
    
    if not input_folder or not os.path.exists(input_folder):
        print("Invalid folder path.")
        return
    
    output_folder = input("Enter output folder (default: summaries): ").strip()
    if not output_folder:
        output_folder = "summaries"
    
    from batch_summarizer import batch_summarize as batch_process
    batch_process(input_folder, output_folder)

def view_logs():
    """Display recent log entries."""
    log_file = "summary_log.txt"
    if not os.path.exists(log_file):
        print("No logs found.")
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print("\n" + "="*50)
        print("RECENT LOGS")
        print("="*50)
        if len(content) > 2000:
            print(content[-2000:])
        else:
            print(content)
        print("="*50)
    except Exception as e:
        print(f"Error reading logs: {str(e)}")

def clear_logs():
    """Clear all log entries."""
    confirm = input("Are you sure you want to clear all logs? (y/n): ").lower()
    if confirm == 'y':
        try:
            open("summary_log.txt", 'w').close()
            print("Logs cleared.")
        except Exception as e:
            print(f"Error clearing logs: {str(e)}")

def main():
    """Main application loop."""
    print("\nWelcome to the Text Summarizer Application!")
    print("Built with Python and OpenAI GPT-3.5")
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            summarize_from_file()
        elif choice == '2':
            summarize_direct_input()
        elif choice == '3':
            batch_summarize()
        elif choice == '4':
            view_logs()
        elif choice == '5':
            clear_logs()
        elif choice == '6':
            print("\nThank you for using the Text Summarizer Application!")
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        print("Please try again or contact support.")
        