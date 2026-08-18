import sys
import os
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

# Make the main LotteryLab project available
# to the mobile application.
if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


# ==========================================================
# DATABASE / PROJECT PATH
# ==========================================================
#
# The desktop LotteryLab database is located at:
#
# C:\Users\User\Lotterylab\data\lottery.db
#
# Changing the working directory here ensures that
# DatabaseManager() used by the mobile screens resolves
# the same database as the desktop application.
#

os.chdir(
    PROJECT_ROOT
)


# ==========================================================
# MOBILE SCREENS
# ==========================================================

from screens.dashboard import DashboardScreen
from screens.ai_generator import AIGeneratorScreen
from screens.statistics import StatisticsScreen
from screens.update import UpdateScreen


class LotteryLabMobile(App):

    # ======================================================
    # BUILD APPLICATION
    # ======================================================

    def build(self):

        self.title = "LotteryLab Mobile"

        # ==================================================
        # ROOT LAYOUT
        # ==================================================

        self.root_layout = BoxLayout(
            orientation="vertical"
        )

        # ==================================================
        # CONTENT AREA
        # ==================================================

        self.content = BoxLayout(
            orientation="vertical"
        )

        self.root_layout.add_widget(
            self.content
        )

        # ==================================================
        # NAVIGATION
        # ==================================================

        navigation = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=60,
            spacing=5,
            padding=5
        )

        # ==================================================
        # DASHBOARD
        # ==================================================

        dashboard_button = Button(
            text="Dashboard"
        )

        dashboard_button.bind(
            on_press=lambda instance:
            self.show_dashboard()
        )

        navigation.add_widget(
            dashboard_button
        )

        # ==================================================
        # AI GENERATOR
        # ==================================================

        ai_button = Button(
            text="AI Generator"
        )

        ai_button.bind(
            on_press=lambda instance:
            self.show_ai()
        )

        navigation.add_widget(
            ai_button
        )

        # ==================================================
        # STATISTICS
        # ==================================================

        statistics_button = Button(
            text="Statistics"
        )

        statistics_button.bind(
            on_press=lambda instance:
            self.show_statistics()
        )

        navigation.add_widget(
            statistics_button
        )

        # ==================================================
        # UPDATE
        # ==================================================

        update_button = Button(
            text="Update"
        )

        update_button.bind(
            on_press=lambda instance:
            self.show_update()
        )

        navigation.add_widget(
            update_button
        )

        # ==================================================
        # ADD NAVIGATION
        # ==================================================

        self.root_layout.add_widget(
            navigation
        )

        # ==================================================
        # START DASHBOARD
        # ==================================================

        self.show_dashboard()

        return self.root_layout

    # ======================================================
    # DASHBOARD
    # ======================================================

    def show_dashboard(self):

        self.content.clear_widgets()

        self.content.add_widget(
            DashboardScreen()
        )

    # ======================================================
    # AI GENERATOR
    # ======================================================

    def show_ai(self):

        self.content.clear_widgets()

        self.content.add_widget(
            AIGeneratorScreen()
        )

    # ======================================================
    # STATISTICS
    # ======================================================

    def show_statistics(self):

        self.content.clear_widgets()

        self.content.add_widget(
            StatisticsScreen()
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def show_update(self):

        self.content.clear_widgets()

        self.content.add_widget(
            UpdateScreen()
        )

    # ======================================================
    # APPLICATION CLOSE
    # ======================================================

    def on_stop(self):

        try:

            for widget in self.content.children:

                if hasattr(
                    widget,
                    "close"
                ):

                    widget.close()

        except Exception:

            pass


# ==========================================================
# START APPLICATION
# ==========================================================

if __name__ == "__main__":

    LotteryLabMobile().run()
    