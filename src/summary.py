"""
LotteryLab Database Summary
"""

import sqlite3
from pathlib import Path

DATABASE_PATH = Path("database") / "lottery.db"


def database_summary():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM powerball_draws")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT MIN(draw_date), MAX(draw_date)
        FROM powerball_draws
    """)

    oldest, newest = cursor.fetchone()

    conn.close()

    print("\n" + "=" * 60)
    print("DATABASE SUMMARY")
    print("=" * 60)
    print(f"Total Draws : {total}")
    print(f"Oldest Draw : {oldest}")
    print(f"Newest Draw : {newest}")


if __name__ == "__main__":
    database_summary()
    