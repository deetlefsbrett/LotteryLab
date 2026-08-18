from collections import Counter
from itertools import combinations


class PairScore:

    """
    Scores tickets based on historical pair frequency.

    Score range:
        0 - 10
    """

    MAX_SCORE = 10.0

    def __init__(self, db):

        self.db = db

        self.counter = Counter()

        self.max_frequency = 0

        self._build()

    # =====================================================
    # BUILD PAIR TABLE
    # =====================================================

    def _build(self):

        draws = self.db.get_all_draws()

        for draw in draws:

            numbers = sorted([
                draw["n1"],
                draw["n2"],
                draw["n3"],
                draw["n4"],
                draw["n5"]
            ])

            for pair in combinations(numbers, 2):

                self.counter[pair] += 1

        if self.counter:

            self.max_frequency = max(
                self.counter.values()
            )

    # =====================================================
    # SCORE PAIR
    # =====================================================

    def score_pair(self, pair):

        if self.max_frequency == 0:

            return 0.0

        pair = tuple(sorted(pair))

        frequency = self.counter.get(pair, 0)

        return (
            frequency / self.max_frequency
        ) * self.MAX_SCORE

    # =====================================================
    # SCORE TICKET
    # =====================================================

    def score_ticket(self, numbers):

        pairs = list(combinations(sorted(numbers), 2))

        if not pairs:

            return 0.0

        total = sum(

            self.score_pair(pair)

            for pair in pairs

        )

        return total / len(pairs)

    # =====================================================
    # TOP PAIRS
    # =====================================================

    def strongest_pairs(self, limit=20):

        return self.counter.most_common(limit)
    