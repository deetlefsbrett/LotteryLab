from collections import Counter


class FrequencyScore:

    """
    Scores numbers based on their historical frequency.

    Score range:
        0 - 20
    """

    MAX_SCORE = 20.0

    def __init__(self, db):

        self.db = db

        self.counter = Counter()

        self.max_frequency = 0

        self._build()

    # =====================================================
    # BUILD FREQUENCY TABLE
    # =====================================================

    def _build(self):

        draws = self.db.get_all_draws()

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
    # SCORE A SINGLE NUMBER
    # =====================================================

    def score_number(self, number):

        if self.max_frequency == 0:

            return 0.0

        frequency = self.counter.get(number, 0)

        return (
            frequency / self.max_frequency
        ) * self.MAX_SCORE

    # =====================================================
    # SCORE A TICKET
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
    # TOP NUMBERS
    # =====================================================

    def top_numbers(self, limit=10):

        return self.counter.most_common(limit)
    