"""
LotteryLab Statistics
"""

import sqlite3
from pathlib import Path
from collections import Counter

DATABASE_PATH = Path("database") / "lottery.db"


def number_frequency():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ball1, ball2, ball3, ball4, ball5
        FROM powerball_draws
    """)

    counter = Counter()

    for row in cursor.fetchall():
        counter.update(row)

    conn.close()

    print("=" * 50)
    print(" TOP 10 MOST FREQUENT MAIN NUMBERS")
    print("=" * 50)

    for number, count in counter.most_common(10):
        print(f"Number {number:>2}: {count} times")


if __name__ == "__main__":
    number_frequency()
    