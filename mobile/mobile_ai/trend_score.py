from collections import Counter


class TrendScore:

    """
    Scores numbers based on recent draws.

    Recent appearances receive higher scores.

    Score range:
        0 - 20
    """

    MAX_SCORE = 20.0

    def __init__(self, db, recent_draws=25):

        self.db = db

        self.recent_draws = recent_draws

        self.counter = Counter()

        self.max_frequency = 0

        self._build()

    # =====================================================
    # BUILD TREND TABLE
    # =====================================================

    def _build(self):

        draws = self.db.get_all_draws()

        if len(draws) > self.recent_draws:
            draws = draws[-self.recent_draws:]

        for draw in draws:

            for i in range(1, 6):

                number = draw[f"n{i}"]

                if number is not None:
                    self.counter[number] += 1

        if self.counter:

            self.max_frequency = max(
                self.counter.values()
            )

    # =====================================================
    # SCORE NUMBER
    # =====================================================

    def score_number(self, number):

        if self.max_frequency == 0:
            return 0.0

        return (
            self.counter.get(number, 0)
            / self.max_frequency
        ) * self.MAX_SCORE

    # =====================================================
    # SCORE TICKET
    # =====================================================

    def score_ticket(self, numbers):

        if not numbers:
            return 0.0

        total = sum(
            self.score_number(number)
            for number in numbers
        )

        return total / len(numbers)

    # =====================================================
    # HOT NUMBERS
    # =====================================================

    def hottest(self, limit=10):

        return self.counter.most_common(limit)
    