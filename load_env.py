import os
from dotenv import load_dotenv

def load_environment_variables():
    """Load environment variables from .env file"""
    # Load .env file if it exists
    load_dotenv()
    
    # Check if GROQ_API_KEY is available
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        print("Warning: GROQ_API_KEY environment variable is not set.")
        print("Please make sure you have a .env file with GROQ_API_KEY=your_api_key")
    
    return groq_api_key
