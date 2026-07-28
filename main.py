from src.database import LotteryDatabase


def main():
    print("=" * 50)
    print("      SA LOTTERY ANALYSIS SUITE")
    print("=" * 50)

    db = LotteryDatabase()

    print("Database connected successfully.")
    print(f"Lotto draws: {db.total_draws('lotto')}")

    db.close()


if __name__ == "__main__":
    main()
    