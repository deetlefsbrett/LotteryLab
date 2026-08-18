import random

from mobile_ai.ai_engine import AIEngine


class PredictionEngine:

    def __init__(self, db):

        self.db = db

        print("Loading Prediction Engine...")

        self.ai = AIEngine(db)

        print("Prediction Engine Ready.")

    # =====================================================
    # STRATEGY SCORE
    # =====================================================

    def strategy_score(
        self,
        ticket,
        strategy
    ):

        frequency = ticket.get(
            "frequency_score",
            0
        )

        trend = ticket.get(
            "trend_score",
            0
        )

        age = ticket.get(
            "age_score",
            0
        )

        pair = ticket.get(
            "pair_score",
            0
        )

        balance = ticket.get(
            "balance_score",
            0
        )

        if strategy == "Balanced":

            return (
                frequency +
                trend +
                age +
                pair +
                balance
            )

        if strategy == "Hot Numbers":

            return (
                frequency * 0.45 +
                trend * 0.35 +
                balance * 0.20
            )

        if strategy == "Trend Focus":

            return (
                trend * 0.50 +
                frequency * 0.25 +
                balance * 0.25
            )

        if strategy == "Overdue Focus":

            return (
                age * 0.55 +
                trend * 0.15 +
                frequency * 0.15 +
                balance * 0.15
            )

        if strategy == "Pair Strength":

            return (
                pair * 0.55 +
                frequency * 0.15 +
                trend * 0.10 +
                balance * 0.20
            )

        return (
            frequency * 0.30 +
            trend * 0.25 +
            age * 0.15 +
            pair * 0.20 +
            balance * 0.10
        )

    # =====================================================
    # GENERATE ONE RANDOM TICKET
    # =====================================================

    def generate_strategy_ticket(
        self,
        strategy="AI Optimized"
    ):

        numbers = sorted(
            random.sample(
                range(1, 51),
                5
            )
        )

        powerball = random.randint(
            1,
            20
        )

        return {
            "numbers": numbers,
            "powerball": powerball,
            "strategy": strategy
        }

    # =====================================================
    # GENERATE AI TICKETS
    # =====================================================

    def generate(
        self,
        amount=10,
        candidate_pool=5000,
        progress_callback=None
    ):

        candidates = []

        total = candidate_pool

        # -------------------------------------------------
        # GENERATE CANDIDATES
        # -------------------------------------------------

        for completed in range(1, total + 1):

            candidate = (
                self.generate_strategy_ticket()
            )

            numbers = candidate["numbers"]

            try:

                analysis = (
                    self.ai.analyse_ticket(
                        numbers
                    )
                )

            except Exception:

                continue

            candidate["score"] = (
                analysis.get(
                    "overall",
                    0
                )
            )

            candidate["details"] = analysis

            candidates.append(
                candidate
            )

            # -------------------------------------------------
            # PROGRESS UPDATE
            # -------------------------------------------------

            if progress_callback is not None:

                percentage = int(
                    completed * 100 / total
                )

                progress_callback(
                    completed,
                    total,
                    percentage
                )

        # -------------------------------------------------
        # SORT BEST TICKETS FIRST
        # -------------------------------------------------

        candidates.sort(
            key=lambda ticket:
            ticket.get("score", 0),
            reverse=True
        )

        # -------------------------------------------------
        # REMOVE DUPLICATES
        # -------------------------------------------------

        results = []

        seen = set()

        for ticket in candidates:

            key = (
                tuple(ticket["numbers"]),
                ticket["powerball"]
            )

            if key in seen:
                continue

            seen.add(key)

            results.append(
                ticket
            )

            if len(results) >= amount:
                break

        return results