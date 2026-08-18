import sys
from pathlib import Path
from collections import Counter

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


# ==========================================================
# STATISTICS CARD
# ==========================================================

class StatisticsCard(BoxLayout):

    def __init__(
        self,
        title,
        lines,
        height=100,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            padding=12,
            spacing=4,
            size_hint_y=None,
            height=height,
            **kwargs
        )

        with self.canvas.before:

            Color(
                0.10,
                0.10,
                0.10,
                1
            )

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[10]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        self.add_widget(
            Label(
                text=title,
                font_size="16sp",
                bold=True,
                size_hint_y=None,
                height=28
            )
        )

        for line in lines:

            self.add_widget(
                Label(
                    text=str(line),
                    font_size="14sp",
                    size_hint_y=None,
                    height=22
                )
            )

    def update_background(self, instance, value):

        self.background.pos = self.pos
        self.background.size = self.size


# ==========================================================
# STATISTICS SCREEN
# ==========================================================

class StatisticsScreen(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=10,
            **kwargs
        )

        self.db = DatabaseManager()

        # ==================================================
        # HEADER
        # ==================================================

        self.add_widget(
            Label(
                text="LOTTERYLAB STATISTICS",
                font_size="28sp",
                bold=True,
                size_hint_y=None,
                height=50
            )
        )

        self.add_widget(
            Label(
                text="PowerBall Historical Analysis",
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
        # REFRESH BUTTON
        # ==================================================

        refresh_button = Button(
            text="REFRESH STATISTICS",
            size_hint_y=None,
            height=55
        )

        refresh_button.bind(
            on_press=self.refresh
        )

        self.add_widget(refresh_button)

        # ==================================================
        # LOAD
        # ==================================================

        self.refresh()

    # ======================================================
    # SECTION TITLE
    # ======================================================

    def section_title(self, text):

        return Label(
            text=text,
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=35,
            halign="left"
        )

    # ======================================================
    # REFRESH
    # ======================================================

    def refresh(self, *args):

        try:

            self.content.clear_widgets()

            draws = self.db.get_all_draws()

            if not draws:

                self.content.add_widget(
                    StatisticsCard(
                        "DATABASE",
                        [
                            "No lottery data available."
                        ],
                        height=90
                    )
                )

                return

            # ==================================================
            # COUNTERS
            # ==================================================

            number_counter = Counter()

            powerball_counter = Counter()

            for draw in draws:

                # ------------------------------------------
                # MAIN NUMBERS
                # ------------------------------------------

                for i in range(1, 6):

                    try:

                        value = draw[f"n{i}"]

                    except (
                        KeyError,
                        IndexError
                    ):

                        value = None

                    if value is not None:

                        number_counter[
                            int(value)
                        ] += 1

                # ------------------------------------------
                # POWERBALL
                # ------------------------------------------

                try:

                    special = draw["special"]

                except (
                    KeyError,
                    IndexError
                ):

                    special = None

                if special is not None:

                    powerball_counter[
                        int(special)
                    ] += 1

            # ==================================================
            # DATABASE SUMMARY
            # ==================================================

            self.content.add_widget(
                self.section_title(
                    "DATABASE SUMMARY"
                )
            )

            self.content.add_widget(
                StatisticsCard(
                    "Historical Data",
                    [
                        f"Total Draws: {len(draws)}",
                        (
                            "Number Entries: "
                            f"{sum(number_counter.values())}"
                        ),
                        (
                            "PowerBall Entries: "
                            f"{sum(powerball_counter.values())}"
                        )
                    ],
                    height=125
                )
            )

            # ==================================================
            # HOT NUMBERS
            # ==================================================

            self.content.add_widget(
                self.section_title(
                    "HOT NUMBERS"
                )
            )

            hot_lines = []

            for rank, (
                number,
                count
            ) in enumerate(
                number_counter.most_common(10),
                start=1
            ):

                hot_lines.append(
                    f"{rank:02}.   "
                    f"{number:02}   -   "
                    f"{count} appearances"
                )

            if not hot_lines:

                hot_lines.append(
                    "No number data available."
                )

            self.content.add_widget(
                StatisticsCard(
                    "Most Frequently Drawn",
                    hot_lines,
                    height=285
                )
            )

            # ==================================================
            # COLD NUMBERS
            # ==================================================

            self.content.add_widget(
                self.section_title(
                    "COLD NUMBERS"
                )
            )

            cold_lines = []

            cold_numbers = sorted(
                number_counter.items(),
                key=lambda x: (
                    x[1],
                    x[0]
                )
            )[:10]

            for rank, (
                number,
                count
            ) in enumerate(
                cold_numbers,
                start=1
            ):

                cold_lines.append(
                    f"{rank:02}.   "
                    f"{number:02}   -   "
                    f"{count} appearances"
                )

            if not cold_lines:

                cold_lines.append(
                    "No number data available."
                )

            self.content.add_widget(
                StatisticsCard(
                    "Least Frequently Drawn",
                    cold_lines,
                    height=285
                )
            )

            # ==================================================
            # POWERBALL FREQUENCY
            # ==================================================

            self.content.add_widget(
                self.section_title(
                    "POWERBALL FREQUENCY"
                )
            )

            powerball_lines = []

            for number in sorted(
                powerball_counter
            ):

                count = powerball_counter[
                    number
                ]

                powerball_lines.append(
                    f"PowerBall {number:02}   -   "
                    f"{count} appearances"
                )

            if not powerball_lines:

                powerball_lines.append(
                    "No PowerBall data available."
                )

            powerball_height = max(
                100,
                55 + (
                    len(powerball_lines) * 22
                )
            )

            self.content.add_widget(
                StatisticsCard(
                    "PowerBall Distribution",
                    powerball_lines,
                    height=powerball_height
                )
            )

            # ==================================================
            # TOP POWERBALL
            # ==================================================

            if powerball_counter:

                (
                    top_powerball,
                    top_count
                ) = powerball_counter.most_common(1)[0]

                self.content.add_widget(
                    self.section_title(
                        "MOST FREQUENT POWERBALL"
                    )
                )

                self.content.add_widget(
                    StatisticsCard(
                        "Top PowerBall",
                        [
                            (
                                f"PowerBall: "
                                f"{top_powerball:02}"
                            ),
                            (
                                f"Appearances: "
                                f"{top_count}"
                            )
                        ],
                        height=100
                    )
                )

            # ==================================================
            # DATA RANGE
            # ==================================================

            latest = self.db.get_latest_draw()

            if latest:

                try:

                    latest_number = latest[
                        "draw_number"
                    ]

                except (
                    KeyError,
                    IndexError
                ):

                    latest_number = "Unknown"

                self.content.add_widget(
                    self.section_title(
                        "LATEST DATA"
                    )
                )

                self.content.add_widget(
                    StatisticsCard(
                        "Current Database",
                        [
                            (
                                f"Latest Draw: "
                                f"{latest_number}"
                            ),
                            "Database status: READY"
                        ],
                        height=100
                    )
                )

        except Exception as error:

            self.content.clear_widgets()

            self.content.add_widget(
                StatisticsCard(
                    "STATISTICS ERROR",
                    [
                        str(error)
                    ],
                    height=110
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
        
