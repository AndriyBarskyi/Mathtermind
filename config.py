# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# UI constants (fixed)
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
SIDEBAR_WIDTH = 64
SIDEBAR_RATIO = 1
CONTENT_RATIO = 18
STYLESHEET_PATH = "src/ui/styles.qss"

# Sensitive data (loaded from .env)
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY")
