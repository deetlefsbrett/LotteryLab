import sqlite3
from pathlib import Path

DATABASE = Path("data/lottery.db")


class LotteryDatabase:

    def __init__(self):
        DATABASE.parent.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotto(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            draw_date TEXT UNIQUE,
            n1 INTEGER,
            n2 INTEGER,
            n3 INTEGER,
            n4 INTEGER,
            n5 INTEGER,
            n6 INTEGER,
            bonus INTEGER
        )
        """)

        self.conn.commit()

    def total_draws(self, table):

        self.cursor.execute(f"SELECT COUNT(*) FROM {table}")

        return self.cursor.fetchone()[0]

    def close(self):

        self.conn.close()
        