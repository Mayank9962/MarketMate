import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")

# Set environment variables for the application
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY 
