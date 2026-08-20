from src.analyzer import Analyzer


class Statistics:

    def __init__(self, db):

        self.db = db
        self.analyzer = Analyzer(db)

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        self.analyzer.refresh()

    # =====================================================
    # DATABASE SUMMARY
    # =====================================================

    def database_summary(self):

        print("\n" + "=" * 60)
        print("POWERBALL DATABASE SUMMARY")
        print("=" * 60)

        print(f"Total Draws     : {self.analyzer.total_draws()}")
        print(f"Numbers Stored  : {self.analyzer.total_numbers()}")

        print("=" * 60)

    # =====================================================
    # HOT NUMBERS
    # =====================================================

    def hot_numbers(self):

        print("\n" + "=" * 60)
        print("TOP 10 HOT NUMBERS")
        print("=" * 60)

        for number, count in self.analyzer.hot_numbers():

            print(f"{number:>2}   {count:>3} times")

    # =====================================================
    # COLD NUMBERS
    # =====================================================

    def cold_numbers(self):

        print("\n" + "=" * 60)
        print("TOP 10 COLD NUMBERS")
        print("=" * 60)

        for number, count in self.analyzer.cold_numbers():

            print(f"{number:>2}   {count:>3} times")

    # =====================================================
    # ODD / EVEN
    # =====================================================

    def odd_even(self):

        odd, even = self.analyzer.odd_even()

        print("\n" + "=" * 60)
        print("ODD / EVEN ANALYSIS")
        print("=" * 60)

        print(f"Odd Numbers  : {odd}")
        print(f"Even Numbers : {even}")

    # =====================================================
    # HIGH / LOW
    # =====================================================

    def high_low(self):

        low, high = self.analyzer.high_low()

        print("\n" + "=" * 60)
        print("HIGH / LOW ANALYSIS")
        print("=" * 60)

        print(f"Low Numbers  : {low}")
        print(f"High Numbers : {high}")

    # =====================================================
    # OVERDUE
    # =====================================================

    def overdue_numbers(self):

        print("\n" + "=" * 60)
        print("TOP 10 OVERDUE NUMBERS")
        print("=" * 60)

        print(f"{'Number':<10}{'Draws Ago'}")
        print("-" * 25)

        for number, draws in self.analyzer.overdue_numbers()[:10]:

            print(f"{number:<10}{draws}")

    # =====================================================
    # PAIR ANALYSIS
    # =====================================================

    def pair_analysis(self):

        pairs = self.analyzer.pair_analysis()

        print("\n" + "=" * 60)
        print("TOP 20 NUMBER PAIRS")
        print("=" * 60)

        if not pairs:
            print("No pair data available.")
            return

        print(f"{'Pair':<15}{'Times'}")
        print("-" * 25)

        for pair, count in pairs:

            print(f"{pair[0]:>2}-{pair[1]:<2}         {count}")

