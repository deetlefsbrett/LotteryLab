from mobile_ai.frequency_score import FrequencyScore
from mobile_ai.trend_score import TrendScore
from mobile_ai.age_score import AgeScore
from mobile_ai.pair_score import PairScore
from mobile_ai.balance_score import BalanceScore
from mobile_ai.confidence_score import ConfidenceScore


class AIEngine:

    def __init__(self, db):

        self.db = db

        print("Loading AI Modules...")

        self.frequency = FrequencyScore(db)
        self.trend = TrendScore(db)
        self.age = AgeScore(db)
        self.pair = PairScore(db)

        self.balance = BalanceScore()

        self.confidence = ConfidenceScore()

        print("AI Ready.")

    # =====================================================
    # SCORE A SINGLE TICKET
    # =====================================================

    def analyse_ticket(self, ticket):

        frequency = self.frequency.score_ticket(ticket)

        trend = self.trend.score_ticket(ticket)

        age = self.age.score_ticket(ticket)

        pair = self.pair.score_ticket(ticket)

        balance = self.balance.score_ticket(ticket)

        overall = self.confidence.calculate(
            frequency,
            trend,
            age,
            pair,
            balance
        )

        breakdown = self.confidence.breakdown(
            frequency,
            trend,
            age,
            pair,
            balance
        )

        recommendation = self.confidence.recommendation(
            overall
        )

        return {

            "ticket": sorted(ticket),

            # Raw scores
            "frequency": round(frequency, 2),
            "trend": round(trend, 2),
            "age": round(age, 2),
            "pair": round(pair, 2),
            "balance": round(balance, 2),

            # Normalized contributions
            "frequency_score": breakdown["frequency"],
            "trend_score": breakdown["trend"],
            "age_score": breakdown["age"],
            "pair_score": breakdown["pair"],
            "balance_score": breakdown["balance"],

            # Final AI score
            "overall": overall,

            "recommendation": recommendation
        }

    # =====================================================
    # SCORE MULTIPLE TICKETS
    # =====================================================

    def analyse_tickets(self, tickets):

        reports = [
            self.analyse_ticket(ticket)
            for ticket in tickets
        ]

        reports.sort(
            key=lambda x: x["overall"],
            reverse=True
        )

        return reports
    
