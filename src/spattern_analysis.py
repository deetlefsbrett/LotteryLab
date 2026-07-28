"""
LotteryLab Pattern Analysis
"""

import sqlite3
from pathlib import Path
from collections import Counter

DATABASE_PATH = Path("database") / "lottery.db"


def odd_even_analysis():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ball1, ball2, ball3, ball4, ball5
        FROM powerball_draws
    """)

    rows = cursor.fetchall()
    conn.close()

    patterns = Counter()

    for row in rows:
        odd = sum(1 for n in row if n % 2 != 0)
        even = 5 - odd
        patterns[f"{odd} Odd / {even} Even"] += 1

    print("\n" + "=" * 60)
    print("ODD / EVEN ANALYSIS")
    print("=" * 60)

    for pattern, count in sorted(patterns.items()):
        print(f"{pattern:<20} {count:>4} draws")


if __name__ == "__main__":
    odd_even_analysis()
    