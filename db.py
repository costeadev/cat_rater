import sqlite3
import os
from pathlib import Path

def get_db_path():
    """Locates or creates a persistent fodler in the user's AppData"""
    if os.name == "nt": # Windows
        base_dir = Path(os.getenv("LOCALAPPDATA")) / "CatRater"
    else: # macOS/Linux
        base_dir = Path.home() / ".catrater"

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / "cats.db"

DB_PATH = get_db_path()

def init_db():
    """Initializes the table structure"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS rated_cats (
                cat_id TEXT PRIMARY KEY,
                url TEXT,
                rating INTEGER,
                date_rated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
def is_cat_rated(cat_id):
    """Checks if a cat ID exists in the database"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM rated_cats WHERE cat_id = ?', (cat_id,))
        return cursor.fetchone() is not None

def save_rating(cat_id, url, rating):
    """Saves or updates a cat's rating"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT OR REPLACE INTO rated_cats (cat_id, url, rating)
            VALUES(?, ?, ?)
        ''', (cat_id, url, rating))