markdown
# Hello Agent Project

A simple AI agent project using OpenAI and Python environment variables.

## Prerequisites

- Python 3.9+
- UV package manager (`pip install uv`)

## Setup Instructions

1. **Create and initialize project**
   ```bash
   uv init hello_agent
   cd hello_agent
Add required dependencies

bash
uv add openai-agents python-dotenv
Create .env file

Create a .env file in your project root with your API key:

env
OPENAI_API_KEY=your-api-key-here
Create main.py

Create a main.py file with:

python
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your agent code here
if __name__ == "__main__":
    print("Hello, AI Agent!")
Run the project

bash
uv run main.py
Project Structure
hello_agent/
├── .env
├── main.py
├── README.md
└── requirements.txt
Notes
Keep your API key secure - never commit the .env file to version control

Add .env to your .gitignore file


To use this setup:

1. Create the `.env` file with:
```bash
echo "OPENAI_API_KEY=your-actual-key-here" > .env
Create the main.py file with the content above

Run with:

bash
uv run main.py
Note: The uv commands might vary slightly depending on your specific UV version. If you encounter any issues, make sure you have the latest version of uv installed (pip install --upgrade uv).

For actual Gemini API usage (instead of OpenAI), you would need to:

Use google-generativeai package instead of openai

Set GEMINI_API_KEY in your .env

Use the appropriate Gemini client initialization