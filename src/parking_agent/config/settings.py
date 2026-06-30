import os

# Base directory is the workspace root (3 levels up from settings.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "db", "parking.db"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
