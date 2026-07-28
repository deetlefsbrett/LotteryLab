"""
LotteryLab Professional GUI
"""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from io import StringIO
import contextlib

from summary import database_summary
from statistics import number_frequency


class LotteryLabGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("LotteryLab Professional")
        self.root.geometry("1200x700")

        self.build_gui()

    # --------------------------------

    def build_gui(self):

        left = tk.Frame(self.root, bg="#2C3E50", width=250)
        left.pack(side="left", fill="y")

        right = tk.Frame(self.root)
        right.pack(side="right", fill="both", expand=True)

        title = tk.Label(
            left,
            text="LotteryLab",
            bg="#2C3E50",
            fg="white",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=20)

        ttk.Button(
            left,
            text="Database Summary",
            command=lambda: self.run_report(database_summary)
        ).pack(fill="x", padx=15, pady=5)

        ttk.Button(
            left,
            text="Number Frequency",
            command=lambda: self.run_report(number_frequency)
        ).pack(fill="x", padx=15, pady=5)

        ttk.Button(
            left,
            text="Charts",
            command=self.show_chart
        ).pack(fill="x", padx=15, pady=5)

        ttk.Button(
            left,
            text="Exit",
            command=self.root.destroy
        ).pack(side="bottom", fill="x", padx=15, pady=20)

        self.results = ScrolledText(
            right,
            font=("Consolas", 11)
        )

        self.results.pack(fill="both", expand=True, padx=10, pady=10)

    # --------------------------------

    def run_report(self, function):

        buffer = StringIO()

        with contextlib.redirect_stdout(buffer):
            function()

        self.results.delete("1.0", tk.END)
        self.results.insert(tk.END, buffer.getvalue())

    # --------------------------------

    def show_chart(self):

        from charts import number_frequency_chart

        number_frequency_chart()


# ======================================

root = tk.Tk()

LotteryLabGUI(root)

root.mainloop()
