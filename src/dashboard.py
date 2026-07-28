"""
LotteryLab Dashboard
"""

from database import create_database
from importer import import_powerball
from statistics import number_frequency


def menu():

    while True:

        print("\n" + "=" * 50)
        print("          LOTTERYLAB DASHBOARD")
        print("=" * 50)

        print("1. Create Database")
        print("2. Import PowerBall Data")
        print("3. Number Frequency Analysis")
        print("4. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            create_database()

        elif choice == "2":
            import_powerball()

        elif choice == "3":
            number_frequency()

        elif choice == "4":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    menu()
    