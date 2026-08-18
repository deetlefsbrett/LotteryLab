class ConfidenceScore:
    """
    Combines the individual AI scoring engines into
    a normalized confidence score out of 100.

    Original scoring ranges:

        Frequency : 0 - 20
        Trend     : 0 - 20
        Age       : 0 - 15
        Pair      : 0 - 10
        Balance   : 0 - 15

    Each component is normalized to a 0 - 20 contribution.

    Final score:
        0 - 100
    """

    FREQUENCY_MAX = 20.0
    TREND_MAX = 20.0
    AGE_MAX = 15.0
    PAIR_MAX = 10.0
    BALANCE_MAX = 15.0

    TARGET_COMPONENT_MAX = 20.0

    def _normalize(self, value, maximum):
        """
        Convert a component score to a 0-20 scale.
        """

        if maximum <= 0:
            return 0.0

        value = max(0.0, min(float(value), maximum))

        return (
            value / maximum
        ) * self.TARGET_COMPONENT_MAX

    # =====================================================
    # CALCULATE CONFIDENCE
    # =====================================================

    def calculate(
        self,
        frequency,
        trend,
        age,
        pair,
        balance
    ):
        frequency_normalized = self._normalize(
            frequency,
            self.FREQUENCY_MAX
        )

        trend_normalized = self._normalize(
            trend,
            self.TREND_MAX
        )

        age_normalized = self._normalize(
            age,
            self.AGE_MAX
        )

        pair_normalized = self._normalize(
            pair,
            self.PAIR_MAX
        )

        balance_normalized = self._normalize(
            balance,
            self.BALANCE_MAX
        )

        total = (
            frequency_normalized +
            trend_normalized +
            age_normalized +
            pair_normalized +
            balance_normalized
        )

        return round(
            min(total, 100.0),
            2
        )

    # =====================================================
    # DETAILED BREAKDOWN
    # =====================================================

    def breakdown(
        self,
        frequency,
        trend,
        age,
        pair,
        balance
    ):
        """
        Returns the normalized contribution of each
        scoring engine.

        Each contribution is 0-20.
        """

        return {
            "frequency": round(
                self._normalize(
                    frequency,
                    self.FREQUENCY_MAX
                ),
                2
            ),

            "trend": round(
                self._normalize(
                    trend,
                    self.TREND_MAX
                ),
                2
            ),

            "age": round(
                self._normalize(
                    age,
                    self.AGE_MAX
                ),
                2
            ),

            "pair": round(
                self._normalize(
                    pair,
                    self.PAIR_MAX
                ),
                2
            ),

            "balance": round(
                self._normalize(
                    balance,
                    self.BALANCE_MAX
                ),
                2
            )
        }

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    def recommendation(self, score):

        if score >= 90:
            return "★★★★★ Exceptional"

        if score >= 80:
            return "★★★★☆ Excellent"

        if score >= 70:
            return "★★★☆☆ Strong"

        if score >= 60:
            return "★★☆☆☆ Average"

        return "★☆☆☆☆ Weak"
    