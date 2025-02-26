"""Configuration settings for the application."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google API settings
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
GMAIL_USER = os.getenv('GMAIL_USER')

# OpenAI settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Shopify settings
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_API_SECRET = os.getenv('SHOPIFY_API_SECRET')
SHOPIFY_STORE_URL = os.getenv('SHOPIFY_STORE_URL')

# Application settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DATA_REFRESH_INTERVAL = int(os.getenv('DATA_REFRESH_INTERVAL', '3600'))  # seconds