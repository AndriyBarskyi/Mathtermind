# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# UI constants (fixed)
WINDOW_WIDTH = 1000  # Increased window width
WINDOW_HEIGHT = 600
SIDEBAR_WIDTH = 240  # Increased sidebar width to accommodate text buttons
SIDEBAR_RATIO = 1
CONTENT_RATIO = 10
STYLESHEET_PATH = "src/ui/styles.qss"

# Sensitive data (loaded from .env)
DATABASE_URL = "sqlite:///mathtermind.db"
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY")
