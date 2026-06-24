# summarizer.py - Summarize text using OpenAI
# This script demonstrates how to use the OpenAI API to summarize articles and text
# Created as part of the AI Research Assistant project

# Import required libraries
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()

# Initialize the OpenAI client with your API key
client = OpenAI()

def summarize(text, max_length=30):
    """
    Summarize the given text using OpenAI's GPT model.
    
    Args:
        text (str): The text to summarize. This can be any length.
        max_length (int): Maximum length of the summary in words. Default is 30.
    
    Returns:
        str: The summarized text, condensed to the specified length.
    
    Example:
        >>> summarize("Python is a programming language that lets you work quickly.", max_length=10)
        'Python is a fast, efficient programming language.'
    """
    try:
        # Create a chat completion request to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that summarizes text concisely in {max_length} words or less."},
                {"role": "user", "content": f"Summarize this: {text}"}
            ]
        )
        
        # Check if the response is empty
        if not response.choices[0].message.content:
            return "Error: Received empty response from the API."
        
        # Extract and return just the summary text
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"

# The code below only runs when you execute this script directly
if __name__ == "__main__":
    
    # Test 1: Short text
    short_text = "Python is a programming language that lets you work quickly and integrate systems more effectively."
    print("Test 1 - Short Text:")
    print(summarize(short_text, max_length=20))
    print()

    # Test 2: Long text - Interstellar Comet article
    long_text = """An interstellar comet that blazed past the sun last year could be nearly three times older than our solar system and is unlike anything ever before seen in our cosmic back yard, astronomers said on Monday.

The comet 3I/Atlas is just the third visitor from beyond our solar system that humanity has ever observed, its unusual brightness offering scientists an unprecedented opportunity to study something that came from elsewhere in the galaxy.

After being spotted in July last year, the space rock prompted excitement online, with one prominent Harvard researcher speculating it could be an alien spacecraft: a theory that Nasa shot down. Now, observations made by the world's most powerful telescopes are revealing more about the unique comet.

According to a study published in the journal Nature, 3I/Atlas could be up to 12bn years old. Our solar system is believed to have formed about 4.5bn years ago.

The lead study author, Martin Cordiner of Nasa's Goddard Space Flight Center, told Agence France-Presse that "maybe it's the oldest object to have been observed in our solar system". However, there could be "edge-case scenarios" that offer other explanations for the comet's unusual chemical composition, he added.

Daniel Lawler
Mon 22 Jun 2026 12.37 EDT"""
    
    print("Test 2 - Long Text (Interstellar Comet Article):")
    print(summarize(long_text, max_length=50))
    print()