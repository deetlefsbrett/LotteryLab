"""
LotteryLab Importer
Imports PowerBall draws from Excel into SQLite.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DATABASE_PATH = Path("database") / "lottery.db"
EXCEL_FILE = Path("data") / "PB_2025.xlsx"


def import_powerball():

    if not EXCEL_FILE.exists():
        print(f"Excel file not found: {EXCEL_FILE}")
        return

    # Read the Excel file
    df = pd.read_excel(EXCEL_FILE, skiprows=2)

    print(f"Rows found: {len(df)}")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    imported = 0
    skipped = 0

    for _, row in df.iterrows():

        try:

            cursor.execute("""
                INSERT OR IGNORE INTO powerball_draws
                (
                    draw_number,
                    draw_date,
                    ball1,
                    ball2,
                    ball3,
                    ball4,
                    ball5,
                    powerball,
                    total_sum
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(row.iloc[0]),      # Draw Number
                str(row.iloc[1]),      # Date
                int(row.iloc[2]),
                int(row.iloc[3]),
                int(row.iloc[4]),
                int(row.iloc[5]),
                int(row.iloc[6]),
                int(row.iloc[7]),
                int(row.iloc[8])
            ))

            if cursor.rowcount == 1:
                imported += 1
            else:
                skipped += 1

        except Exception as e:
            print(f"Skipped row بسبب error: {e}")

    conn.commit()
    conn.close()

    print()
    print("==========================")
    print(" Import Complete")
    print("==========================")
    print(f"Imported : {imported}")
    print(f"Skipped  : {skipped}")


if __name__ == "__main__":
    import_powerball()
    """
LotteryLab Importer
Imports PowerBall draws from Excel into SQLite.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DATABASE_PATH = Path("database") / "lottery.db"
EXCEL_FILE = Path("data") / "PB_2025.xlsx"


def import_powerball():

    if not EXCEL_FILE.exists():
        print(f"Excel file not found: {EXCEL_FILE}")
        return

    # Read the Excel file
    df = pd.read_excel(EXCEL_FILE, skiprows=2)

    print(f"Rows found: {len(df)}")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    imported = 0
    skipped = 0

    for _, row in df.iterrows():

        try:

            cursor.execute("""
                INSERT OR IGNORE INTO powerball_draws
                (
                    draw_number,
                    draw_date,
                    ball1,
                    ball2,
                    ball3,
                    ball4,
                    ball5,
                    powerball,
                    total_sum
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(row.iloc[0]),      # Draw Number
                str(row.iloc[1]),      # Date
                int(row.iloc[2]),
                int(row.iloc[3]),
                int(row.iloc[4]),
                int(row.iloc[5]),
                int(row.iloc[6]),
                int(row.iloc[7]),
                int(row.iloc[8])
            ))

            if cursor.rowcount == 1:
                imported += 1
            else:
                skipped += 1

        except Exception as e:
            print(f"Skipped row duerror: {e}")

    conn.commit()
    conn.close()

    print()
    print("==========================")
    print(" Import Complete")
    print("==========================")
    print(f"Imported : {imported}")
    print(f"Skipped  : {skipped}")


if __name__ == "__main__":
    import_powerball()
    