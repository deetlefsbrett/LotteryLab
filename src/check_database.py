import sqlite3
from pathlib import Path

DATABASE_PATH = Path("database") / "lottery.db"

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM powerball_draws")
count = cursor.fetchone()[0]

print(f"Total records: {count}")

conn.close()
