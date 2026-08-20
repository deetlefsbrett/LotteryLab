import time

from src.downloader import LotteryDownloader
from src.backup import DatabaseBackup


class LotteryUpdater:

    def __init__(self, db):

        self.db = db
        self.downloader = LotteryDownloader()
        self.backup = DatabaseBackup()

    # =====================================================
    # LOG MESSAGE
    # =====================================================

    def log(self, message, callback=None):

        print(message)

        if callback:
            callback(message)

    # =====================================================
    # UPDATE DATABASE
    # =====================================================

    def update(self, callback=None):

        self.log("\n" + "=" * 60, callback)
        self.log("AUTOMATIC POWERBALL UPDATE", callback)
        self.log("=" * 60, callback)

        # ---------------------------------------------
        # Backup
        # ---------------------------------------------

        self.log(
            "Creating database backup...",
            callback
        )

        self.backup.create_backup()
        self.backup.cleanup()

        self.log(
            "Backup completed.",
            callback
        )

        # ---------------------------------------------
        # Find latest draw
        # ---------------------------------------------

        latest_database = self.db.latest_draw_number()

        self.log(
            f"Latest draw in database : {latest_database}",
            callback
        )

        next_draw = latest_database + 1

        added = 0

        # Safety limit.
        # We never want the updater to run forever.
        max_checks = 5

        # ---------------------------------------------
        # Download loop
        # ---------------------------------------------

        for attempt in range(max_checks):

            self.log(
                f"Checking draw {next_draw} "
                f"({attempt + 1}/{max_checks})...",
                callback
            )

            try:

                draw = self.downloader.get_draw(
                    next_draw
                )

            except Exception as error:

                self.log(
                    f"Error checking draw {next_draw}: "
                    f"{error}",
                    callback
                )

                break

            # -----------------------------------------
            # No draw returned
            # -----------------------------------------

            if draw is None:

                self.log(
                    "No newer draws found.",
                    callback
                )

                break

            # -----------------------------------------
            # Validate returned draw number
            # -----------------------------------------

            returned_number = draw.get(
                "draw_number"
            )

            if returned_number is None:

                self.log(
                    "API returned invalid draw data.",
                    callback
                )

                break

            # -----------------------------------------
            # Prevent unexpected API loop
            # -----------------------------------------

            if returned_number <= latest_database:

                self.log(
                    f"API returned draw "
                    f"{returned_number}, which is not newer "
                    f"than database draw "
                    f"{latest_database}.",
                    callback
                )

                break

            # -----------------------------------------
            # Already exists
            # -----------------------------------------

            if self.db.draw_exists(
                returned_number
            ):

                self.log(
                    f"Draw {returned_number} already exists.",
                    callback
                )

                next_draw = returned_number + 1

                continue

            # -----------------------------------------
            # Validate numbers
            # -----------------------------------------

            numbers = draw.get(
                "numbers",
                []
            )

            powerball = draw.get(
                "powerball"
            )

            if len(numbers) != 5:

                self.log(
                    f"Invalid number set returned for "
                    f"draw {returned_number}.",
                    callback
                )

                break

            if powerball is None:

                self.log(
                    f"No PowerBall number returned for "
                    f"draw {returned_number}.",
                    callback
                )

                break

            # -----------------------------------------
            # Add draw
            # -----------------------------------------

            self.db.add_draw(
                game="POWERBALL",
                draw_number=returned_number,
                draw_date=draw["draw_date"],
                numbers=numbers,
                special=powerball
            )

            self.db.log_update(
                "POWERBALL",
                returned_number,
                "SUCCESS",
                "Downloaded from Official API"
            )

            added += 1

            latest_database = returned_number
            next_draw = returned_number + 1

            self.log(
                f"Added draw {returned_number}",
                callback
            )

            time.sleep(0.5)

        # ---------------------------------------------
        # Summary
        # ---------------------------------------------

        self.log(
            "\n" + "=" * 60,
            callback
        )

        if added == 0:

            self.log(
                "Database already up to date.",
                callback
            )

        else:

            self.log(
                f"{added} new draw(s) added.",
                callback
            )

        self.log(
            "=" * 60,
            callback
        )

        return added
