# setup.py - Run this once to install all required libraries

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = [
    "openai",
    "python-dotenv",
    "langchain",
    "langchain-community",
    "chromadb",
    "pypdf",
    "tiktoken",
    "streamlit",
    "beautifulsoup4",
    "requests",
    "scikit-learn",
    "pandas",
    "plotly",
]

print("Installing packages...")
for pkg in packages:
    print(f"Installing {pkg}...")
    install(pkg)

print("All packages installed successfully!")
