"""
LotteryLab Charts
"""

import sqlite3
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

DATABASE_PATH = Path("database") / "lottery.db"


def number_frequency_chart():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ball1, ball2, ball3, ball4, ball5
        FROM powerball_draws
    """)

    rows = cursor.fetchall()
    conn.close()

    counter = Counter()

    for row in rows:
        counter.update(row)

    numbers = list(range(1, 51))
    counts = [counter[n] for n in numbers]

    plt.figure(figsize=(12, 6))
    plt.bar(numbers, counts)

    plt.title("Main Number Frequency")
    plt.xlabel("Number")
    plt.ylabel("Times Drawn")

    plt.xticks(range(1, 51, 2))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    number_frequency_chart()
    