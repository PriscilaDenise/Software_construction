import logging
from logger_config import setup_logger
from storage import load_data
from auth import login
from transactions import deposit, withdraw, view_balance, change_password
from reports import bank_summary, transaction_history
from exceptions import BankingError, AuthenticationError, DataStorageError

setup_logger()
logger = logging.getLogger(__name__)


def user_menu(data, username):
    while True:
        print("\n========== BANK MENU ==========")
        print("1. Make a Deposit")
        print("2. Make a Withdrawal")
        print("3. View Balance")
        print("4. View Bank Summary")
        print("5. View Transaction History")
        print("6. Change Password")
        print("7. Logout")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                deposit(data, username)
            elif choice == "2":
                withdraw(data, username)
            elif choice == "3":
                view_balance(data, username)
            elif choice == "4":
                bank_summary(data, username)
            elif choice == "5":
                transaction_history(data, username)
            elif choice == "6":
                change_password(data, username)
            elif choice == "7":
                logger.info("User logged out: %s", username)
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please select a valid option.")

        except BankingError as error:
            logger.error("Operation error for %s: %s", username, error)
            print(f"Error: {error}")


def main():
    try:
        data = load_data()
    except DataStorageError as error:
        logger.critical("Application startup failed: %s", error)
        print(f"Fatal error: {error}")
        return

    while True:
        print("\n========== SIMPLE BANKING SYSTEM ==========")
        print("1. Login")
        print("2. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            try:
                username = login(data)
                user_menu(data, username)
            except AuthenticationError as error:
                print(error)
        elif choice == "2":
            logger.info("Application closed by user.")
            print("Thank you for using the banking system.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()