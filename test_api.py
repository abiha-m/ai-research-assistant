# test_api.py - Test your OpenAI API key

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Say 'I am ready to build AI projects!'"}]
)

print(response.choices[0].message.content)
