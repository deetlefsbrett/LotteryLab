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
# INFORMATION CARD
# ==========================================================

class InfoCard(BoxLayout):

    def __init__(
        self,
        title,
        value,
        subtitle="",
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            padding=12,
            spacing=3,
            size_hint_y=None,
            height=105,
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
                font_size="13sp",
                size_hint_y=None,
                height=25
            )
        )

        self.add_widget(
            Label(
                text=str(value),
                font_size="25sp",
                bold=True,
                size_hint_y=None,
                height=38
            )
        )

        if subtitle:

            self.add_widget(
                Label(
                    text=subtitle,
                    font_size="12sp",
                    size_hint_y=None,
                    height=22
                )
            )

    def update_background(self, instance, value):

        self.background.pos = self.pos
        self.background.size = self.size


# ==========================================================
# DASHBOARD
# ==========================================================

class DashboardScreen(BoxLayout):

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
                text="LOTTERYLAB MOBILE",
                font_size="28sp",
                bold=True,
                size_hint_y=None,
                height=50
            )
        )

        self.add_widget(
            Label(
                text="South African PowerBall Intelligence",
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

        scroll.add_widget(self.content)

        self.add_widget(scroll)

        # ==================================================
        # REFRESH
        # ==================================================

        refresh_button = Button(
            text="REFRESH DASHBOARD",
            size_hint_y=None,
            height=55
        )

        refresh_button.bind(
            on_press=self.refresh
        )

        self.add_widget(refresh_button)

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
    # SAFE ROW VALUE
    # ======================================================

    def row_value(self, row, *names):

        for name in names:

            try:
                return row[name]
            except (KeyError, IndexError):
                pass

        return None

    # ======================================================
    # REFRESH
    # ======================================================

    def refresh(self, *args):

        try:

            self.content.clear_widgets()

            draws = self.db.get_all_draws()

            if not draws:

                self.content.add_widget(
                    Label(
                        text=(
                            "No lottery data is available "
                            "in the database."
                        ),
                        font_size="17sp",
                        size_hint_y=None,
                        height=100
                    )
                )

                return

            # ==================================================
            # DATABASE INFORMATION
            # ==================================================

            total_draws = len(draws)

            latest = self.db.get_latest_draw()

            try:
                last_update = self.db.get_last_update()
            except Exception:
                last_update = "Not available"

            # ==================================================
            # FREQUENCY ANALYSIS
            # ==================================================

            number_counter = Counter()
            powerball_counter = Counter()

            for draw in draws:

                for i in range(1, 6):

                    try:
                        value = draw[f"n{i}"]
                    except (KeyError, IndexError):
                        value = None

                    if value is not None:

                        number_counter[
                            int(value)
                        ] += 1

                try:
                    special = draw["special"]
                except (KeyError, IndexError):
                    special = None

                if special is not None:

                    powerball_counter[
                        int(special)
                    ] += 1

            # ==================================================
            # HOT NUMBER
            # ==================================================

            if number_counter:

                hot_number, hot_count = (
                    number_counter.most_common(1)[0]
                )

            else:

                hot_number = 0
                hot_count = 0

            # ==================================================
            # COLD NUMBER
            # ==================================================

            if number_counter:

                cold_number, cold_count = sorted(
                    number_counter.items(),
                    key=lambda x: (
                        x[1],
                        x[0]
                    )
                )[0]

            else:

                cold_number = 0
                cold_count = 0

            # ==================================================
            # TOP POWERBALL
            # ==================================================

            if powerball_counter:

                (
                    top_powerball,
                    top_powerball_count
                ) = powerball_counter.most_common(1)[0]

            else:

                top_powerball = 0
                top_powerball_count = 0

            # ==================================================
            # DATABASE STATUS
            # ==================================================

            self.content.add_widget(
                self.section_title(
                    "DATABASE STATUS"
                )
            )

            self.content.add_widget(
                InfoCard(
                    "DATABASE",
                    "CONNECTED",
                    f"{total_draws} draws loaded"
                )
            )

            # ==================================================
            # QUICK INTELLIGENCE
            # ==================================================

            self.content.add_widget(
                self.section_title(
                    "QUICK INTELLIGENCE"
                )
            )

            stats_row = BoxLayout(
                orientation="horizontal",
                spacing=8,
                size_hint_y=None,
                height=105
            )

            stats_row.add_widget(
                InfoCard(
                    "HOT NUMBER",
                    f"{hot_number:02}",
                    f"{hot_count} appearances"
                )
            )

            stats_row.add_widget(
                InfoCard(
                    "COLD NUMBER",
                    f"{cold_number:02}",
                    f"{cold_count} appearances"
                )
            )

            stats_row.add_widget(
                InfoCard(
                    "TOP POWERBALL",
                    f"{top_powerball:02}",
                    f"{top_powerball_count} appearances"
                )
            )

            self.content.add_widget(stats_row)

            # ==================================================
            # LATEST DRAW
            # ==================================================

            self.content.add_widget(
                self.section_title(
                    "LATEST POWERBALL DRAW"
                )
            )

            if latest:

                draw_number = self.row_value(
                    latest,
                    "draw_number",
                    "draw"
                )

                draw_date = self.row_value(
                    latest,
                    "draw_date",
                    "date",
                    "drawDate"
                )

                numbers = []

                for i in range(1, 6):

                    value = self.row_value(
                        latest,
                        f"n{i}"
                    )

                    if value is not None:

                        numbers.append(
                            f"{int(value):02}"
                        )

                special = self.row_value(
                    latest,
                    "special",
                    "powerball",
                    "power_ball"
                )

                if draw_number is None:
                    draw_number = "Unknown"

                if draw_date is None:
                    draw_date = "Date unavailable"

                draw_card = BoxLayout(
                    orientation="vertical",
                    padding=15,
                    spacing=5,
                    size_hint_y=None,
                    height=180
                )

                with draw_card.canvas.before:

                    Color(
                        0.10,
                        0.10,
                        0.10,
                        1
                    )

                    draw_background = RoundedRectangle(
                        pos=draw_card.pos,
                        size=draw_card.size,
                        radius=[10]
                    )

                draw_card.bind(
                    pos=lambda instance, value:
                    self.update_card_background(
                        draw_background,
                        instance
                    ),
                    size=lambda instance, value:
                    self.update_card_background(
                        draw_background,
                        instance
                    )
                )

                draw_card.add_widget(
                    Label(
                        text=(
                            f"Draw {draw_number}    "
                            f"{draw_date}"
                        ),
                        font_size="14sp",
                        size_hint_y=None,
                        height=30
                    )
                )

                draw_card.add_widget(
                    Label(
                        text="   ".join(numbers),
                        font_size="28sp",
                        bold=True,
                        size_hint_y=None,
                        height=55
                    )
                )

                if special is not None:

                    draw_card.add_widget(
                        Label(
                            text=(
                                f"POWERBALL: "
                                f"{int(special):02}"
                            ),
                            font_size="19sp",
                            bold=True,
                            size_hint_y=None,
                            height=35
                        )
                    )

                self.content.add_widget(draw_card)

            else:

                self.content.add_widget(
                    Label(
                        text="No latest draw available.",
                        size_hint_y=None,
                        height=70
                    )
                )

            # ==================================================
            # SYSTEM STATUS
            # ==================================================

            self.content.add_widget(
                self.section_title(
                    "SYSTEM STATUS"
                )
            )

            system_card = BoxLayout(
                orientation="vertical",
                padding=12,
                spacing=3,
                size_hint_y=None,
                height=120
            )

            with system_card.canvas.before:

                Color(
                    0.10,
                    0.10,
                    0.10,
                    1
                )

                system_background = RoundedRectangle(
                    pos=system_card.pos,
                    size=system_card.size,
                    radius=[10]
                )

            system_card.bind(
                pos=lambda instance, value:
                self.update_card_background(
                    system_background,
                    instance
                ),
                size=lambda instance, value:
                self.update_card_background(
                    system_background,
                    instance
                )
            )

            system_card.add_widget(
                Label(
                    text="Database       READY",
                    font_size="14sp"
                )
            )

            system_card.add_widget(
                Label(
                    text="AI Engine      READY",
                    font_size="14sp"
                )
            )

            system_card.add_widget(
                Label(
                    text="Updater        READY",
                    font_size="14sp"
                )
            )

            self.content.add_widget(system_card)

            # ==================================================
            # LAST UPDATE
            # ==================================================

            self.content.add_widget(
                Label(
                    text=(
                        f"Last database update: "
                        f"{last_update}"
                    ),
                    font_size="12sp",
                    size_hint_y=None,
                    height=30
                )
            )

        except Exception as error:

            self.content.clear_widgets()

            self.content.add_widget(
                Label(
                    text=(
                        "LOTTERYLAB DASHBOARD\n\n"
                        "DATABASE ERROR\n\n"
                        f"{error}"
                    ),
                    font_size="16sp",
                    size_hint_y=None,
                    height=150
                )
            )

    # ======================================================
    # CARD BACKGROUND
    # ======================================================

    def update_card_background(
        self,
        background,
        widget
    ):

        background.pos = widget.pos
        background.size = widget.size

    # ======================================================
    # CLEANUP
    # ======================================================

    def close(self):

        try:
            self.db.close()
        except Exception:
            pass
        
