class BalanceScore:
    """
    Scores a ticket based on how well balanced it is.

    Categories:
        • Odd / Even
        • Low / High
        • Decade Spread

    Score range:
        0 - 15
    """

    MAX_SCORE = 15.0

    def score_ticket(self, numbers):

        score = 0.0

        # -----------------------------------
        # Odd / Even
        # -----------------------------------

        odd = sum(1 for n in numbers if n % 2)

        even = len(numbers) - odd

        if (odd, even) in (
            (3, 2),
            (2, 3)
        ):
            score += 5

        elif (odd, even) in (
            (4, 1),
            (1, 4)
        ):
            score += 3

        else:
            score += 1

        # -----------------------------------
        # Low / High
        # -----------------------------------

        low = sum(1 for n in numbers if n <= 25)

        high = len(numbers) - low

        if (low, high) in (
            (3, 2),
            (2, 3)
        ):
            score += 5

        elif (low, high) in (
            (4, 1),
            (1, 4)
        ):
            score += 3

        else:
            score += 1

        # -----------------------------------
        # Decade Spread
        # -----------------------------------

        decades = set()

        for number in numbers:

            decade = (number - 1) // 10

            decades.add(decade)

        score += min(
            len(decades),
            5
        )

        return min(
            score,
            self.MAX_SCORE
        )
    