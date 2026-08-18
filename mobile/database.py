import sqlite3
from pathlib import Path
from datetime import datetime


class DatabaseManager:

    """
    Android-safe LotteryLab mobile database.

    The database is stored in the application's writable
    data directory when running on Android.

    When running the mobile application on Windows for testing,
    the database is stored in:

        LotteryLab/mobile/data/lottery.db
    """

    def __init__(self):

        # ==================================================
        # DETERMINE DATABASE LOCATION
        # ==================================================

        try:

            from kivy.app import App

            app = App.get_running_app()

        except Exception:

            app = None

        if app is not None:

            # Android / Kivy application storage
            base_path = Path(app.user_data_dir)

        else:

            # Windows development/testing
            base_path = (
                Path(__file__).resolve().parent
                / "data"
            )

        base_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.database = (
            base_path / "lottery.db"
        )

        # ==================================================
        # SQLITE CONNECTION
        # ==================================================

        self.conn = sqlite3.connect(
            str(self.database),
            check_same_thread=False
        )

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        self.create_tables()

    # =====================================================
    # CREATE TABLES
    # =====================================================

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS draws (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                game TEXT NOT NULL,

                draw_number INTEGER,

                draw_date TEXT NOT NULL,

                n1 INTEGER,
                n2 INTEGER,
                n3 INTEGER,
                n4 INTEGER,
                n5 INTEGER,
                n6 INTEGER,

                special INTEGER,

                UNIQUE(game, draw_number)

            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS update_history (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                update_time TEXT,

                game TEXT,

                draw_number INTEGER,

                status TEXT,

                notes TEXT

            )
        """)

        self.conn.commit()

    # =====================================================
    # ADD DRAW
    # =====================================================

    def add_draw(
        self,
        game,
        draw_number,
        draw_date,
        numbers,
        special
    ):

        numbers = list(numbers)

        while len(numbers) < 6:
            numbers.append(None)

        self.cursor.execute("""
            INSERT OR IGNORE INTO draws
            (
                game,
                draw_number,
                draw_date,
                n1,
                n2,
                n3,
                n4,
                n5,
                n6,
                special
            )

            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """,
        (
            game,
            draw_number,
            draw_date,
            numbers[0],
            numbers[1],
            numbers[2],
            numbers[3],
            numbers[4],
            numbers[5],
            special
        ))

        self.conn.commit()

    # =====================================================
    # DRAW COUNT
    # =====================================================

    def get_draw_count(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM draws
            WHERE game = 'POWERBALL'
        """)

        result = self.cursor.fetchone()

        return result[0] if result else 0

    # =====================================================
    # LATEST DRAW
    # =====================================================

    def get_latest_draw(self):

        self.cursor.execute("""
            SELECT
                game,
                draw_number,
                draw_date,
                n1,
                n2,
                n3,
                n4,
                n5,
                n6,
                special

            FROM draws

            WHERE game = 'POWERBALL'

            ORDER BY
                draw_date DESC,
                draw_number DESC

            LIMIT 1
        """)

        row = self.cursor.fetchone()

        if row is None:
            return None

        return {
            "game": row["game"],
            "draw_number": row["draw_number"],
            "draw_date": row["draw_date"],
            "date": row["draw_date"],
            "numbers": [
                row["n1"],
                row["n2"],
                row["n3"],
                row["n4"],
                row["n5"]
            ],
            "powerball": row["special"]
        }

    # =====================================================
    # LATEST DRAW NUMBER
    # =====================================================

    def latest_draw_number(
        self,
        game="POWERBALL"
    ):

        self.cursor.execute("""
            SELECT MAX(draw_number)

            FROM draws

            WHERE game = ?
        """, (game,))

        result = self.cursor.fetchone()

        if result is None:
            return 0

        return result[0] or 0

    # =====================================================
    # DRAW EXISTS
    # =====================================================

    def draw_exists(
        self,
        draw_number,
        game="POWERBALL"
    ):

        self.cursor.execute("""
            SELECT COUNT(*)

            FROM draws

            WHERE game = ?
            AND draw_number = ?
        """,
        (
            game,
            draw_number
        ))

        result = self.cursor.fetchone()

        return (
            result is not None
            and result[0] > 0
        )

    # =====================================================
    # LAST UPDATE
    # =====================================================

    def get_last_update(self):

        self.cursor.execute("""
            SELECT MAX(update_time)
            FROM update_history
        """)

        result = self.cursor.fetchone()

        if result and result[0]:
            return result[0]

        return "No updates recorded"

    # =====================================================
    # ALL DRAWS
    # =====================================================

    def get_all_draws(
        self,
        game="POWERBALL"
    ):

        self.cursor.execute("""
            SELECT *

            FROM draws

            WHERE game = ?

            ORDER BY
                draw_date,
                draw_number
        """, (game,))

        return self.cursor.fetchall()

    # =====================================================
    # RECENT DRAWS
    # =====================================================

    def get_recent_draws(
        self,
        limit=10,
        game="POWERBALL"
    ):

        self.cursor.execute("""
            SELECT *

            FROM draws

            WHERE game = ?

            ORDER BY
                draw_date DESC,
                draw_number DESC

            LIMIT ?
        """,
        (
            game,
            limit
        ))

        return self.cursor.fetchall()

    # =====================================================
    # UPDATE HISTORY
    # =====================================================

    def log_update(
        self,
        game,
        draw_number,
        status,
        notes=""
    ):

        self.cursor.execute("""
            INSERT INTO update_history
            (
                update_time,
                game,
                draw_number,
                status,
                notes
            )

            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """,
        (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            game,
            draw_number,
            status,
            notes
        ))

        self.conn.commit()

    # =====================================================
    # RECENT UPDATES
    # =====================================================

    def get_recent_updates(
        self,
        limit=10
    ):

        self.cursor.execute("""
            SELECT *

            FROM update_history

            ORDER BY id DESC

            LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    # =====================================================
    # DATABASE PATH
    # =====================================================

    def get_database_path(self):

        return str(
            self.database
        )

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        try:

            if self.conn:
                self.conn.close()

        except Exception:

            pass
        