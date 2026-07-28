"""
LotteryLab PowerBall Statistics
"""

import sqlite3
from pathlib import Path
from collections import Counter

DATABASE_PATH = Path("database") / "lottery.db"


def powerball_frequency():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT powerball
        FROM powerball_draws
    """)

    rows = cursor.fetchall()

    conn.close()

    counter = Counter()

    for row in rows:
        counter.update(row)

    print("\n" + "=" * 60)
    print("POWERBALL ANALYSIS")
    print("=" * 60)

    print(f"\nTotal Draws Analysed : {len(rows)}")

    print("\nPowerBall   Times Drawn")
    print("-" * 30)

    for number in range(1, 21):
        print(f"{number:>5} {counter[number]:>14}")

    most = counter.most_common(1)[0]
    least = min(counter.items(), key=lambda x: x[1])

    print("\nMost Frequent PowerBall")
    print("-----------------------")
    print(f"{most[0]} drawn {most[1]} times")

    print("\nLeast Frequent PowerBall")
    print("------------------------")
    print(f"{least[0]} drawn {least[1]} times")


if __name__ == "__main__":
    powerball_frequency()
    