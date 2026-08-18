class AgeScore:

    """
    Scores numbers based on how long ago they appeared.

    Older numbers receive higher scores.

    Score range:
        0 - 15
    """

    MAX_SCORE = 15.0

    def __init__(self, db):

        self.db = db

        self.number_age = {}

        self.max_age = 0

        self._build()

    # =====================================================
    # BUILD AGE TABLE
    # =====================================================

    def _build(self):

        draws = self.db.get_all_draws()

        latest_index = len(draws)

        last_seen = {}

        for index, draw in enumerate(draws, start=1):

            for i in range(1, 6):

                number = draw[f"n{i}"]

                if number is not None:

                    last_seen[number] = index

        for number in range(1, 51):

            age = latest_index - last_seen.get(number, 0)

            self.number_age[number] = age

        if self.number_age:

            self.max_age = max(
                self.number_age.values()
            )

    # =====================================================
    # SCORE NUMBER
    # =====================================================

    def score_number(self, number):

        if self.max_age == 0:

            return 0.0

        age = self.number_age.get(number, 0)

        return (
            age / self.max_age
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
    # MOST OVERDUE
    # =====================================================

    def most_overdue(self, limit=10):

        return sorted(
            self.number_age.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
    