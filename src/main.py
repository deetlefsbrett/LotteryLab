"""
LotteryLab
Version 1.0
Main Application
"""

from datetime import datetime


def show_banner():
    print("=" * 50)
    print("        LOTTERYLAB v1.0")
    print("=" * 50)
    print(f"Started: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print()


def show_menu():
    print("1. Import Historical Results")
    print("2. Database Summary")
    print("3. Number Statistics")
    print("4. Generate Numbers")
    print("5. Exit")
    print()


def main():
    show_banner()

    while True:
        show_menu()

        choice = input("Select an option (1-5): ")

        if choice == "1":
            print("\nImport module coming soon...\n")

        elif choice == "2":
            print("\nDatabase module coming soon...\n")

        elif choice == "3":
            print("\nStatistics module coming soon...\n")

        elif choice == "4":
            print("\nGenerator module coming soon...\n")

        elif choice == "5":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option.\n")


if __name__ == "__main__":
    main()
    