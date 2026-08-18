import sys
import threading
from pathlib import Path

from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar


# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from database import DatabaseManager
from mobile_ai.prediction_engine import PredictionEngine


# ==========================================================
# TICKET CARD
# ==========================================================

class TicketCard(BoxLayout):

    def __init__(
        self,
        ticket_number,
        numbers,
        powerball,
        score,
        recommendation,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=8,
            size_hint_y=None,
            height=210,
            **kwargs
        )

        with self.canvas.before:
            Color(0.10, 0.10, 0.10, 1)

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[12]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # Header

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=35
        )

        header.add_widget(
            Label(
                text=f"TICKET #{ticket_number}",
                font_size="18sp",
                bold=True,
                halign="left"
            )
        )

        header.add_widget(
            Label(
                text=f"AI SCORE: {score:.1f}",
                font_size="17sp",
                bold=True,
                halign="right"
            )
        )

        self.add_widget(header)

        # Numbers

        number_text = "   ".join(
            f"{int(number):02}"
            for number in numbers
        )

        self.add_widget(
            Label(
                text=number_text,
                font_size="27sp",
                bold=True,
                size_hint_y=None,
                height=50
            )
        )

        # PowerBall

        self.add_widget(
            Label(
                text=f"POWERBALL 🔴 {int(powerball):02}",
                font_size="19sp",
                bold=True,
                size_hint_y=None,
                height=35
            )
        )

        # Recommendation

        self.add_widget(
            Label(
                text=str(recommendation),
                font_size="15sp",
                size_hint_y=None,
                height=30
            )
        )

    def update_background(self, instance, value):

        self.background.pos = self.pos
        self.background.size = self.size


# ==========================================================
# AI GENERATOR SCREEN
# ==========================================================

class AIGeneratorScreen(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",
            padding=15,
            spacing=10,
            **kwargs
        )

        # Database

        self.db = DatabaseManager()

        self.engine = PredictionEngine(
            self.db
        )

        self.generating = False
        self.current_tickets = []

        # ==================================================
        # HEADER
        # ==================================================

        self.add_widget(
            Label(
                text="AI TICKET GENERATOR",
                font_size="27sp",
                bold=True,
                size_hint_y=None,
                height=55
            )
        )

        self.add_widget(
            Label(
                text="LotteryLab PowerBall Intelligence",
                font_size="15sp",
                size_hint_y=None,
                height=35
            )
        )

        # ==================================================
        # CONTROLS
        # ==================================================

        controls = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=55,
            spacing=10
        )

        self.ticket_count = Spinner(
            text="10",
            values=(
                "5",
                "10",
                "20",
                "50"
            ),
            size_hint_x=0.35
        )

        controls.add_widget(
            self.ticket_count
        )

        self.generate_button = Button(
            text="🎯 GENERATE AI TICKETS",
            size_hint_x=0.65
        )

        self.generate_button.bind(
            on_press=self.generate_tickets
        )

        controls.add_widget(
            self.generate_button
        )

        self.add_widget(
            controls
        )

        # ==================================================
        # PROGRESS PERCENTAGE
        # ==================================================

        self.progress_label = Label(
            text="Progress: 0%",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height=30
        )

        self.add_widget(
            self.progress_label
        )

        # ==================================================
        # PROGRESS BAR
        # ==================================================

        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=20
        )

        self.add_widget(
            self.progress_bar
        )

        # ==================================================
        # CANDIDATE COUNT
        # ==================================================

        self.candidate_label = Label(
            text="Candidates: 0 / 5,000",
            font_size="14sp",
            size_hint_y=None,
            height=28
        )

        self.add_widget(
            self.candidate_label
        )

        # ==================================================
        # STATUS
        # ==================================================

        self.status = Label(
            text="Ready",
            font_size="15sp",
            size_hint_y=None,
            height=35
        )

        self.add_widget(
            self.status
        )

        # ==================================================
        # RESULTS
        # ==================================================

        self.results = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=(0, 5),
            size_hint_y=None
        )

        self.results.bind(
            minimum_height=self.results.setter(
                "height"
            )
        )

        scroll = ScrollView()

        scroll.add_widget(
            self.results
        )

        self.add_widget(
            scroll
        )

        self.show_message(
            "Generate AI tickets to begin."
        )

    # ======================================================
    # MESSAGE
    # ======================================================

    def show_message(self, message):

        self.results.clear_widgets()

        self.results.add_widget(
            Label(
                text=message,
                font_size="17sp",
                size_hint_y=None,
                height=100,
                halign="center",
                valign="middle"
            )
        )

    # ======================================================
    # GENERATE BUTTON
    # ======================================================

    def generate_tickets(self, *args):

        if self.generating:
            return

        amount = int(
            self.ticket_count.text
        )

        self.generating = True

        self.generate_button.disabled = True

        self.generate_button.text = (
            "ANALYSING..."
        )

        self.progress_bar.value = 0

        self.progress_label.text = (
            "Progress: 0%"
        )

        self.candidate_label.text = (
            "Candidates: 0 / 5,000"
        )

        self.status.text = (
            "LotteryLab AI is analysing "
            "historical data..."
        )

        self.show_message(
            "Running AI analysis...\n\n"
            "Please wait."
        )

        thread = threading.Thread(
            target=self.run_generation,
            args=(amount,),
            daemon=True
        )

        thread.start()

    # ======================================================
    # RUN AI ENGINE
    # ======================================================

    def run_generation(self, amount):

        worker_db = None

        try:

            worker_db = DatabaseManager()

            worker_engine = PredictionEngine(
                worker_db
            )

            tickets = worker_engine.generate(
                amount=amount,
                candidate_pool=5000,
                progress_callback=self.generation_progress
            )

            Clock.schedule_once(
                lambda dt: self.generation_complete(
                    tickets
                ),
                0
            )

        except Exception as error:

            # IMPORTANT:
            # Copy the exception into a normal variable.
            # Python clears the exception variable after
            # the except block, so it cannot be captured
            # directly by a delayed lambda.

            error_message = str(error)

            Clock.schedule_once(
                lambda dt, message=error_message:
                self.generation_error(message),
                0
            )

        finally:

            if worker_db is not None:

                try:
                    worker_db.close()

                except Exception:
                    pass

    # ======================================================
    # PROGRESS CALLBACK
    # ======================================================

    def generation_progress(
        self,
        completed,
        total,
        percentage
    ):

        Clock.schedule_once(
            lambda dt,
                   completed=completed,
                   total=total,
                   percentage=percentage:
            self.update_progress(
                completed,
                total,
                percentage
            ),
            0
        )

    # ======================================================
    # UPDATE PROGRESS
    # ======================================================

    def update_progress(
        self,
        completed,
        total,
        percentage
    ):

        if not self.generating:
            return

        self.progress_bar.value = percentage

        self.progress_label.text = (
            f"Progress: {percentage}%"
        )

        self.candidate_label.text = (
            f"Candidates: "
            f"{completed:,} / {total:,}"
        )

        self.status.text = (
            f"AI analysing candidates... "
            f"{percentage}%"
        )

    # ======================================================
    # GENERATION COMPLETE
    # ======================================================

    def generation_complete(self, tickets):

        self.progress_bar.value = 100

        self.progress_label.text = (
            "Progress: 100%"
        )

        self.candidate_label.text = (
            "Candidates: 5,000 / 5,000"
        )

        self.generating = False

        self.generate_button.disabled = False

        self.generate_button.text = (
            "🎯 GENERATE AI TICKETS"
        )

        self.current_tickets = tickets

        if not tickets:

            self.status.text = (
                "No tickets generated."
            )

            self.show_message(
                "The AI engine did not return "
                "any valid tickets."
            )

            return

        self.display_tickets(
            tickets
        )

    # ======================================================
    # DISPLAY TICKETS
    # ======================================================

    def display_tickets(self, tickets):

        self.results.clear_widgets()

        for index, ticket in enumerate(
            tickets,
            start=1
        ):

            numbers = ticket.get(
                "numbers",
                []
            )

            powerball = ticket.get(
                "powerball",
                0
            )

            score = ticket.get(
                "score",
                0
            )

            details = ticket.get(
                "details",
                {}
            )

            recommendation = details.get(
                "recommendation",
                "AI analysis complete"
            )

            card = TicketCard(
                ticket_number=index,
                numbers=numbers,
                powerball=powerball,
                score=score,
                recommendation=recommendation
            )

            self.results.add_widget(
                card
            )

        self.status.text = (
            f"{len(tickets)} AI tickets generated"
        )

    # ======================================================
    # GENERATION ERROR
    # ======================================================

    def generation_error(self, error):

        self.generating = False

        self.generate_button.disabled = False

        self.generate_button.text = (
            "🎯 GENERATE AI TICKETS"
        )

        self.progress_label.text = (
            "Progress: Error"
        )

        self.status.text = (
            "AI generation failed."
        )

        self.show_message(
            "AI GENERATION ERROR\n\n"
            f"{error}"
        )

    # ======================================================
    # CLEANUP
    # ======================================================

    def close(self):

        try:
            self.db.close()

        except Exception:
            pass