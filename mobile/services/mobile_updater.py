import time
import requests
from datetime import datetime, timezone, timedelta


class MobileUpdater:

    # ======================================================
    # NATIONAL LOTTERY POWERBALL API
    # ======================================================

    API_URL = (
        "https://www.nationallottery.co.za/"
        "api/engine/draw/getIssueDrawResultDetail"
    )

    GAME_ID = 11201
    WIN_POOL_ID = 100

    # We have confirmed this from the live National Lottery
    # website on 17 August 2026.
    #
    # Issue 1746 = PowerBall draw on 14 August 2026.
    #
    # This is an API issue number, NOT our database draw number.
    KNOWN_CURRENT_ISSUE = 1746

    def __init__(self, db):

        self.db = db

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/149.0 Safari/537.36"
            ),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://www.nationallottery.co.za",
            "Referer": "https://www.nationallottery.co.za/"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    # ======================================================
    # GET ONE API ISSUE
    # ======================================================

    def get_draw(self, issue):

        payload = {
            "gameId": self.GAME_ID,
            "issue": int(issue),
            "winPoolId": self.WIN_POOL_ID,
            "plusFlag": 0,
            "platform": 4,
            "deviceCode": "1",
            "deviceSoftVersion": "1.0.0",
            "timestamp": int(time.time() * 1000)
        }

        try:

            response = self.session.post(
                self.API_URL,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            if data.get("code") != 0:
                return None

            result = data.get("data")

            if not result:
                return None

            notice = result.get("winNotice")

            if not notice:
                return None

            api_issue = notice.get("issue")

            draw_time = notice.get("drawTime")

            win_nums = notice.get("winNums", [])

            if not api_issue or not draw_time:
                return None

            numbers = []
            powerball = None

            for item in win_nums:

                try:
                    number = int(item["winNum"])
                except Exception:
                    continue

                flag = int(
                    item.get("winNumFlag", 0)
                )

                if flag == 0:
                    numbers.append(number)

                elif flag == 1:
                    powerball = number

            # PowerBall must contain exactly 5 main numbers
            # and one PowerBall number.
            if len(numbers) != 5:
                return None

            if powerball is None:
                return None

            # --------------------------------------------------
            # Convert API date to YYYY-MM-DD
            # --------------------------------------------------

            draw_date = str(draw_time)[:10]

            return {
                "api_issue": int(api_issue),
                "draw_number": int(api_issue),
                "draw_date": draw_date,
                "numbers": sorted(numbers),
                "powerball": powerball
            }

        except requests.RequestException as error:

            print(
                f"Network error checking API issue "
                f"{issue}: {error}"
            )

            return None

        except Exception as error:

            print(
                f"API error checking issue "
                f"{issue}: {error}"
            )

            return None

    # ======================================================
    # FIND CURRENT API ISSUE
    # ======================================================

    def find_latest_api_issue(self, callback=None):

        def log(message):

            print(message)

            if callback:
                callback(message)

        # Start at the confirmed current issue.
        issue = self.KNOWN_CURRENT_ISSUE

        log(
            f"Checking confirmed API issue {issue}..."
        )

        draw = self.get_draw(issue)

        if draw:

            log(
                f"Confirmed API issue {issue}: "
                f"{draw['draw_date']}"
            )

        # --------------------------------------------------
        # Look forward for newer completed draws.
        #
        # We allow several attempts because future issues
        # will appear as new draws are published.
        # --------------------------------------------------

        latest = draw

        for test_issue in range(
            issue + 1,
            issue + 10
        ):

            log(
                f"Checking API issue "
                f"{test_issue}..."
            )

            candidate = self.get_draw(
                test_issue
            )

            if candidate is None:

                break

            latest = candidate

            time.sleep(0.25)

        if latest:

            log(
                f"Latest available API issue: "
                f"{latest['api_issue']} "
                f"({latest['draw_date']})"
            )

            return latest["api_issue"]

        return None

    # ======================================================
    # FIND DATABASE LAST DATE
    # ======================================================

    def get_database_latest_date(self):

        try:

            latest = self.db.get_latest_draw()

            if not latest:
                return None

            # Our DatabaseManager returns "date".
            value = latest.get("date")

            if not value:
                return None

            return str(value)[:10]

        except Exception as error:

            print(
                f"Could not determine database "
                f"latest date: {error}"
            )

            return None

    # ======================================================
    # ADD DRAW
    # ======================================================

    def save_draw(self, draw):

        try:

            self.db.add_draw(
                game="POWERBALL",
                draw_number=draw["api_issue"],
                draw_date=draw["draw_date"],
                numbers=draw["numbers"],
                special=draw["powerball"]
            )

            try:

                self.db.log_update(
                    "POWERBALL",
                    draw["api_issue"],
                    "SUCCESS",
                    (
                        "Downloaded from official "
                        "National Lottery API"
                    )
                )

            except Exception:
                pass

            return True

        except Exception as error:

            print(
                f"Database error saving issue "
                f"{draw['api_issue']}: {error}"
            )

            return False

    # ======================================================
    # UPDATE
    # ======================================================

    def update(self, callback=None):

        def log(message):

            print(message)

            if callback:
                callback(str(message))

        log(
            "========================================"
        )

        log(
            "LOTTERYLAB MOBILE POWERBALL UPDATE"
        )

        log(
            "========================================"
        )

        # --------------------------------------------------
        # DATABASE STATUS
        # --------------------------------------------------

        latest_db_date = (
            self.get_database_latest_date()
        )

        latest_db_issue = 0

        try:

            latest_db_issue = (
                self.db.latest_draw_number()
            )

        except Exception:

            pass

        log(
            f"Database latest draw number: "
            f"{latest_db_issue}"
        )

        log(
            f"Database latest date: "
            f"{latest_db_date or 'No data'}"
        )

        # --------------------------------------------------
        # FIND LATEST API ISSUE
        # --------------------------------------------------

        latest_api_issue = (
            self.find_latest_api_issue(
                callback=callback
            )
        )

        if latest_api_issue is None:

            log(
                "Unable to determine the latest "
                "PowerBall API issue."
            )

            return 0

        log(
            f"Latest API issue available: "
            f"{latest_api_issue}"
        )

        # --------------------------------------------------
        # IMPORTANT
        #
        # Our old database may contain the old numbering
        # system. Therefore we cannot use:
        #
        #     latest_db_issue + 1
        #
        # to determine the API issue.
        #
        # Instead we work from the known API issue 1746
        # backwards until we reach the database date,
        # then forward again.
        # --------------------------------------------------

        target_issue = latest_api_issue

        # --------------------------------------------------
        # If database is empty, download a useful history.
        #
        # For your current situation we only need to recover
        # the missing draws around July/August.
        # --------------------------------------------------

        if latest_db_date is None:

            log(
                "Database contains no PowerBall data."
            )

            # Start from a reasonable historical window.
            start_issue = max(
                1,
                target_issue - 30
            )

        else:

            # --------------------------------------------------
            # We know issue 1746 = 14 Aug 2026.
            #
            # Work backwards from the current API issue
            # until we reach the database's latest date.
            # --------------------------------------------------

            start_issue = target_issue

            for issue in range(
                target_issue,
                max(0, target_issue - 100),
                -1
            ):

                draw = self.get_draw(issue)

                if draw is None:
                    continue

                log(
                    f"Checking history issue "
                    f"{issue}: "
                    f"{draw['draw_date']}"
                )

                if draw["draw_date"] <= latest_db_date:

                    start_issue = issue + 1

                    break

                time.sleep(0.2)

        # --------------------------------------------------
        # SAFETY
        # --------------------------------------------------

        if start_issue < 1:

            start_issue = 1

        log(
            f"Starting catch-up at API issue "
            f"{start_issue}"
        )

        added = 0

        # --------------------------------------------------
        # DOWNLOAD MISSING ISSUES
        # --------------------------------------------------

        for issue in range(
            start_issue,
            target_issue + 1
        ):

            log(
                f"Checking API issue {issue}..."
            )

            draw = self.get_draw(issue)

            if draw is None:

                log(
                    f"No result available for "
                    f"API issue {issue}."
                )

                continue

            # --------------------------------------------------
            # Avoid duplicates
            #
            # We now use the API issue as the database
            # draw_number as well.
            # --------------------------------------------------

            try:

                if self.db.draw_exists(
                    draw["api_issue"]
                ):

                    log(
                        f"Issue "
                        f"{draw['api_issue']} "
                        "already exists."
                    )

                    continue

            except Exception:

                pass

            # --------------------------------------------------
            # Save
            # --------------------------------------------------

            if self.save_draw(draw):

                added += 1

                log(
                    f"ADDED: "
                    f"Issue {draw['api_issue']} | "
                    f"{draw['draw_date']} | "
                    f"{' '.join(f'{n:02}' for n in draw['numbers'])} | "
                    f"PB {draw['powerball']:02}"
                )

            time.sleep(0.5)

        # --------------------------------------------------
        # FINAL STATUS
        # --------------------------------------------------

        log(
            "========================================"
        )

        if added == 0:

            log(
                "No new PowerBall draws were added."
            )

        else:

            log(
                f"{added} new PowerBall "
                f"draw(s) added."
            )

        log(
            "========================================"
        )

        return added

    # ======================================================
    # CLOSE
    # ======================================================

    def close(self):

        try:
            self.session.close()
        except Exception:
            pass
        