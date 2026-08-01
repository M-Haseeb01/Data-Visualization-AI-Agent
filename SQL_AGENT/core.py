"""
Core utilities for SQL Agent.
"""

import os
import shutil
import uuid

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

GROQ_MODEL = "llama-3.3-70b-versatile"

DATABASE_DIR = "databases"
os.makedirs(DATABASE_DIR, exist_ok=True)


def save_database(file_obj):
    """
    Save uploaded SQLite database and return its path.
    """

    if file_obj is None:
        raise ValueError("Please upload a SQLite database.")

    source = file_obj if isinstance(file_obj, str) else file_obj.name

    extension = os.path.splitext(source)[1].lower()

    if extension not in [".db", ".sqlite", ".sqlite3"]:
        raise ValueError(
            "Unsupported database. Please upload .db, .sqlite, or .sqlite3."
        )

    filename = f"db_{uuid.uuid4().hex}{extension}"
    destination = os.path.join(DATABASE_DIR, filename)

    shutil.copy2(source, destination)

    return destination
