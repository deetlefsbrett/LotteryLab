import sys
import threading
from pathlib import Path

from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent.parent
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from database import DatabaseManager
from services.mobile_updater import MobileUpdater


# ==========================================================
# UPDATE SCREEN
# ==========================================================

class UpdateScreen(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=10,
            **kwargs
        )

        # --------------------------------------------------
        # Main UI database connection
        # --------------------------------------------------

        self.db = DatabaseManager()

        # --------------------------------------------------
        # IMPORTANT:
        #
        # Do NOT use this database connection from the
        # background update thread.
        #
        # A separate DatabaseManager will be created inside
        # run_update().
        # --------------------------------------------------

        self.updating = False
        self.messages = []

        # ==================================================
        # HEADER
        # ==================================================

        self.add_widget(
            Label(
                text="LOTTERYLAB UPDATE",
                font_size="28sp",
                bold=True,
                size_hint_y=None,
                height=50
            )
        )

        self.add_widget(
            Label(
                text="Official South African PowerBall Results",
                font_size="15sp",
                size_hint_y=None,
                height=32
            )
        )

        # ==================================================
        # SCROLL AREA
        # ==================================================

        scroll = ScrollView()

        self.content = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=(0, 5),
            size_hint_y=None
        )

        self.content.bind(
            minimum_height=self.content.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.content
        )

        self.add_widget(scroll)

        # ==================================================
        # UPDATE BUTTON
        # ==================================================

        self.update_button = Button(
            text="UPDATE NOW",
            size_hint_y=None,
            height=60
        )

        self.update_button.bind(
            on_press=self.start_update
        )

        self.add_widget(
            self.update_button
        )

        # ==================================================
        # INITIAL STATUS
        # ==================================================

        self.show_database_status()

    # ======================================================
    # CARD
    # ======================================================

    def create_card(
        self,
        title,
        lines,
        height=120
    ):

        card = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=5,
            size_hint_y=None,
            height=height
        )

        with card.canvas.before:

            Color(
                0.10,
                0.10,
                0.10,
                1
            )

            background = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[10]
            )

        card.bind(
            pos=lambda instance, value:
            self.update_background(
                background,
                instance
            ),
            size=lambda instance, value:
            self.update_background(
                background,
                instance
            )
        )

        card.add_widget(
            Label(
                text=title,
                font_size="17sp",
                bold=True,
                size_hint_y=None,
                height=30
            )
        )

        for line in lines:

            card.add_widget(
                Label(
                    text=str(line),
                    font_size="14sp",
                    size_hint_y=None,
                    height=22
                )
            )

        return card

    # ======================================================
    # BACKGROUND
    # ======================================================

    def update_background(
        self,
        background,
        widget
    ):

        background.pos = widget.pos
        background.size = widget.size

    # ======================================================
    # DATABASE STATUS
    # ======================================================

    def show_database_status(self):

        try:

            self.content.clear_widgets()

            draws = self.db.get_draw_count()

            latest = self.db.get_latest_draw()

            try:

                last_update = (
                    self.db.get_last_update()
                )

            except Exception:

                last_update = "Not available"

            lines = []

            lines.append(
                f"Total Draws: {draws}"
            )

            if latest:

                try:

                    draw_number = latest[
                        "draw_number"
                    ]

                except (
                    KeyError,
                    IndexError
                ):

                    draw_number = "Unknown"

                try:

                    draw_date = latest[
                        "draw_date"
                    ]

                except (
                    KeyError,
                    IndexError
                ):

                    draw_date = "Date unavailable"

                lines.append(
                    f"Latest Draw: {draw_number}"
                )

                lines.append(
                    f"Draw Date: {draw_date}"
                )

            else:

                lines.append(
                    "Latest Draw: No data"
                )

            lines.append(
                f"Last Update: {last_update}"
            )

            self.content.add_widget(
                Label(
                    text="DATABASE STATUS",
                    font_size="17sp",
                    bold=True,
                    size_hint_y=None,
                    height=35
                )
            )

            self.content.add_widget(
                self.create_card(
                    "Database",
                    lines,
                    height=135
                )
            )

            self.content.add_widget(
                Label(
                    text="UPDATE SERVICE",
                    font_size="17sp",
                    bold=True,
                    size_hint_y=None,
                    height=35
                )
            )

            self.content.add_widget(
                self.create_card(
                    "Official Results",
                    [
                        "Source: South African PowerBall",
                        "Status: READY",
                        "Internet connection required"
                    ],
                    height=110
                )
            )

        except Exception as error:

            self.content.clear_widgets()

            self.content.add_widget(
                self.create_card(
                    "DATABASE ERROR",
                    [
                        str(error)
                    ],
                    height=100
                )
            )

    # ======================================================
    # START UPDATE
    # ======================================================

    def start_update(self, *args):

        if self.updating:
            return

        self.updating = True

        self.messages = []

        self.update_button.disabled = True
        self.update_button.text = "UPDATING..."

        self.content.clear_widgets()

        self.content.add_widget(
            Label(
                text="UPDATE IN PROGRESS",
                font_size="18sp",
                bold=True,
                size_hint_y=None,
                height=40
            )
        )

        self.content.add_widget(
            self.create_card(
                "PowerBall Update",
                [
                    "Starting updater...",
                    "",
                    "Please wait."
                ],
                height=110
            )
        )

        thread = threading.Thread(
            target=self.run_update,
            daemon=True
        )

        thread.start()

    # ======================================================
    # RUN UPDATE
    # ======================================================

    def run_update(self):

        update_db = None

        try:

            # ==================================================
            # IMPORTANT SQLITE FIX
            #
            # This DatabaseManager is CREATED INSIDE the
            # background thread.
            #
            # Therefore its SQLite connection belongs to
            # this thread.
            # ==================================================

            update_db = DatabaseManager()

            updater = MobileUpdater(
                update_db
            )

            # --------------------------------------------------
            # Callback
            # --------------------------------------------------

            def callback(message):

                message = str(message)

                self.messages.append(
                    message
                )

                Clock.schedule_once(
                    lambda dt:
                    self.update_status(),
                    0
                )

            # --------------------------------------------------
            # Run updater
            # --------------------------------------------------

            added = updater.update(
                callback=callback
            )

            # --------------------------------------------------
            # Close background DB connection
            # --------------------------------------------------

            try:

                update_db.close()

            except Exception:

                pass

            update_db = None

            # --------------------------------------------------
            # Return result to Kivy main thread
            # --------------------------------------------------

            Clock.schedule_once(
                lambda dt,
                result=added:
                self.update_finished(result),
                0
            )

        except Exception as error:

            error_message = str(error)

            # --------------------------------------------------
            # Make absolutely sure the worker DB is closed
            # --------------------------------------------------

            if update_db is not None:

                try:

                    update_db.close()

                except Exception:

                    pass

            # --------------------------------------------------
            # Return error to main Kivy thread
            # --------------------------------------------------

            Clock.schedule_once(
                lambda dt,
                message=error_message:
                self.update_error(message),
                0
            )

    # ======================================================
    # LIVE STATUS
    # ======================================================

    def update_status(self):

        if not self.messages:
            return

        self.content.clear_widgets()

        self.content.add_widget(
            Label(
                text="UPDATE IN PROGRESS",
                font_size="18sp",
                bold=True,
                size_hint_y=None,
                height=40
            )
        )

        self.content.add_widget(
            self.create_card(
                "Live Update Status",
                self.messages,
                height=max(
                    110,
                    60 + len(self.messages) * 24
                )
            )
        )

    # ======================================================
    # UPDATE FINISHED
    # ======================================================

    def update_finished(self, added):

        self.updating = False

        self.update_button.disabled = False
        self.update_button.text = "UPDATE NOW"

        try:

            # --------------------------------------------------
            # This database connection belongs to the Kivy
            # main thread, so it is safe to use here.
            # --------------------------------------------------

            draws = self.db.get_draw_count()

            latest = self.db.get_latest_draw()

            lines = [
                f"New Draws Added: {added}",
                f"Total Draws: {draws}"
            ]

            if latest:

                try:

                    draw_number = latest[
                        "draw_number"
                    ]

                except (
                    KeyError,
                    IndexError
                ):

                    draw_number = "Unknown"

                lines.append(
                    f"Latest Draw: {draw_number}"
                )

            if added == 0:

                lines.append(
                    "Database was already up to date."
                )

            else:

                lines.append(
                    f"{added} new draw(s) downloaded."
                )

            self.content.clear_widgets()

            self.content.add_widget(
                Label(
                    text="UPDATE COMPLETE",
                    font_size="19sp",
                    bold=True,
                    size_hint_y=None,
                    height=40
                )
            )

            self.content.add_widget(
                self.create_card(
                    "Update Result",
                    lines,
                    height=145
                )
            )

            self.content.add_widget(
                Label(
                    text="Database is ready.",
                    font_size="14sp",
                    size_hint_y=None,
                    height=35
                )
            )

        except Exception as error:

            self.update_error(
                "Update completed, but the database "
                "status could not be refreshed.\n\n"
                f"{error}"
            )

    # ======================================================
    # UPDATE ERROR
    # ======================================================

    def update_error(self, error):

        self.updating = False

        self.update_button.disabled = False
        self.update_button.text = "UPDATE NOW"

        self.content.clear_widgets()

        self.content.add_widget(
            Label(
                text="UPDATE ERROR",
                font_size="19sp",
                bold=True,
                size_hint_y=None,
                height=40
            )
        )

        self.content.add_widget(
            self.create_card(
                "Unable to Update",
                [
                    str(error),
                    "",
                    "Check the update status "
                    "and try again."
                ],
                height=150
            )
        )

    # ======================================================
    # CLEANUP
    # ======================================================

    def close(self):

        try:

            self.db.close()

        except Exception:

            pass
        
