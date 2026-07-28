"""
LotteryLab Hot & Cold Numbers
"""

import sqlite3
from pathlib import Path
from collections import Counter

DATABASE_PATH = Path("database") / "lottery.db"


def hot_cold_numbers():

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

    print("\n" + "=" * 60)
    print("HOT & COLD NUMBERS")
    print("=" * 60)

    print("\n🔥 HOT NUMBERS")
    print("-" * 25)

    for number, count in counter.most_common(10):
        print(f"{number:>2}  ->  {count} times")

    print("\n❄️ COLD NUMBERS")
    print("-" * 25)

    cold = sorted(counter.items(), key=lambda x: x[1])[:10]

    for number, count in cold:
        print(f"{number:>2}  ->  {count} times")


if __name__ == "__main__":
    hot_cold_numbers()
    