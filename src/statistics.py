"""
LotteryLab Statistics Module
Author: Brett Deetlefs
Version: 1.0
"""

import sqlite3
from pathlib import Path
from collections import Counter

# ----------------------------------------------------
# Database Location
# ----------------------------------------------------

DATABASE_PATH = Path("database") / "lottery.db"


# ----------------------------------------------------
# Get Number Frequencies
# ----------------------------------------------------

def get_number_frequencies():

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

    return counter, len(rows)


# ----------------------------------------------------
# Display Report
# ----------------------------------------------------

def number_frequency():

    counter, total_draws = get_number_frequencies()

    print("\n")
    print("=" * 65)
    print("             LOTTERYLAB NUMBER ANALYSIS")
    print("=" * 65)

    print(f"Total Draws Analysed : {total_draws}")
    print(f"Total Numbers Drawn  : {total_draws * 5}")

    print("\nNUMBER FREQUENCIES")
    print("-" * 30)

    print(f"{'Number':<10}{'Times Drawn'}")

    for number in range(1, 51):
        print(f"{number:<10}{counter[number]}")

    print("\n")
    print("=" * 65)
    print("TOP 10 HOT NUMBERS")
    print("=" * 65)

    for number, count in counter.most_common(10):
        print(f"Number {number:>2}   {count} times")

    print("\n")
    print("=" * 65)
    print("TOP 10 COLD NUMBERS")
    print("=" * 65)

    cold = sorted(counter.items(), key=lambda item: item[1])[:10]

    for number, count in cold:
        print(f"Number {number:>2}   {count} times")


# ----------------------------------------------------
# Main
# ----------------------------------------------------

if __name__ == "__main__":
    number_frequency()
    