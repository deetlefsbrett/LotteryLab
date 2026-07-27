"""
LotteryLab Database Module
Creates and manages the SQLite database.
"""

import sqlite3
from pathlib import Path

# Database location
DATABASE_PATH = Path("database") / "lottery.db"


def create_database():
    """Create the database and the draws table."""

    # Create the database folder if it doesn't exist
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS draws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL,
            draw_number INTEGER,
            draw_date TEXT NOT NULL,
            ball1 INTEGER,
            ball2 INTEGER,
            ball3 INTEGER,
            ball4 INTEGER,
            ball5 INTEGER,
            bonus_ball INTEGER,
            total_sum INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")
    print(f"Location: {DATABASE_PATH.resolve()}")


if __name__ == "__main__":
    create_database()
    """
LotteryLab Database Module
"""

import sqlite3
from pathlib import Path

DATABASE_PATH = Path("database") / "lottery.db"


def create_database():

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS powerball_draws (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            draw_number INTEGER UNIQUE,

            draw_date TEXT,

            ball1 INTEGER,
            ball2 INTEGER,
            ball3 INTEGER,
            ball4 INTEGER,
            ball5 INTEGER,

            powerball INTEGER,

            total_sum INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database ready.")


if __name__ == "__main__":
    create_database()
    