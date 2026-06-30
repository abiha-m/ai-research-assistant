# Technical Design Document: Text Summarizer

## 1. Overview

This document describes the technical design of the Text Summarizer application, built as Project 1 of an AI engineering portfolio.

## 2. Architecture

### High-Level Architecture

### Components

1. **Menu Interface** (`app.py`)
   - Handles user interaction
   - Displays menu options
   - Routes user requests to appropriate functions

2. **Core Summarizer** (`summarizer.py`)
   - `summarize(text, max_length)`: Main summarization function
   - `read_file(file_path)`: Reads text from files
   - `save_summary(text, output_path)`: Saves summaries to files
   - `log_summary(input_text, output_text)`: Logs operations

3. **Batch Processor** (`batch_summarizer.py`)
   - Processes all .txt files in a folder
   - Handles errors per file
   - Creates output summaries

## 3. Data Flow

1. User selects an option from the menu
2. Application collects input (file path or direct text)
3. Input is validated
4. OpenAI API is called with the text
5. Summary is generated and returned
6. Summary is displayed to the user
7. Operation is logged to `summary_log.txt`
8. Optionally, summary is saved to a file

## 4. Error Handling Strategy

The application handles these error types:
- Missing or invalid API key
- Empty or short text input
- File not found
- API rate limiting or quota issues
- Network errors
- Generic exceptions

Each error is caught, logged, and displayed as a friendly message to the user.

## 5. API Integration

- Provider: OpenAI
- Model: gpt-3.5-turbo
- Purpose: Text summarization
- Parameters: temperature=0.5, max_tokens=200
- Cost Management: Token counting is tracked via logging

## 6. Security Considerations

- API key is stored in `.env` file (not in version control)
- `.gitignore` prevents `.env` from being committed
- No user data is stored permanently (only logs summary operations)

## 7. Testing Strategy

- Unit testing: Each function is tested independently
- Integration testing: Full workflow tested from menu to output
- Edge case testing: Empty input, very long input, malformed files

## 8. Future Improvements

- Add support for PDF and DOCX files
- Add caching to reduce API calls and costs
- Add a graphical user interface (Streamlit)
- Add multiple summarization styles (concise, detailed, bullet points)
- Add language detection and summarization in multiple languages

## 9. Lessons Learned

1. **Error handling is essential** - A robust application needs to handle all possible errors gracefully.
2. **Logging helps debugging** - Having a log file made it much easier to track issues.
3. **Testing each function** independently saved time when debugging the full application.
4. **Git workflow** - Learning add, commit, push was essential for tracking progress.
