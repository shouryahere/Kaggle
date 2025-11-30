"""
Configuration module for Life Admin Concierge Agent.
Load API keys and settings from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Google Cloud Configuration (for Calendar/Gmail)
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

# Agent Configuration
DEFAULT_MODEL = "gemini-2.0-flash"
MAX_TOKENS = 8192
TEMPERATURE = 0.7

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENABLE_OBSERVABILITY = True

# Session Configuration
SESSION_TIMEOUT_MINUTES = 30
