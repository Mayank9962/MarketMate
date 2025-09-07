import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBYZTXwbDlRMGxZli64cAaCgyaPFJNCwXw")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "0d3443760308836f5f53f6ad35ef67aa6c9a7790d044ae254c1f036b5ec555b4")

# Set environment variables for the application
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY 