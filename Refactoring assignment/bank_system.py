import json
import os
from datetime import datetime

DATA_FILE = "bank_data.json"


def load_data():
    """Load banking data from JSON file or create default data if file does not exist."""
    if not os.path.exists(DATA_FILE):
        default_data = {
            "clients": {
                "emma001": {
                    "password": "1234",
                    "full_name": "Emmanuel Nsubuga",
                    "account_number": "100001",
                    "balance": 500000.0,
                    "transactions": [
                        {
                            "type": "Initial Deposit",
                            "amount": 500000.0,
                            "time": current_time()
                        }
                    ]
                },
                "sarah001": {
                    "password": "abcd",
                    "full_name": "Sarah Namusoke",
                    "account_number": "100002",
                    "balance": 300000.0,
                    "transactions": [
                        {
                            "type": "Initial Deposit",
                            "amount": 300000.0,
                            "time": current_time()
                        }
                    ]
                }
            }
        }
        save_data(default_data)
        return default_data

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Error reading data file. A new one will be created.")
        default_data = {"clients": {}}
        save_data(default_data)
        return default_data


def save_data(data):
    """Save banking data to JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except IOError:
        print("Error saving data.")


def current_time():
    """Return the current date and time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def login(data):
    """Prompt the user to log in and return the username if successful."""
    print("\n========== BANK LOGIN ==========")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    client = data["clients"].get(username)

    if client and client["password"] == password:
        print(f"\nLogin successful. Welcome, {client['full_name']}!")
        return username

    print("\nInvalid username or password.")
    return None


def deposit(data, username):
    """Allow the logged-in user to deposit money."""
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Deposit amount must be greater than 0.")
            return

        data["clients"][username]["balance"] += amount
        data["clients"][username]["transactions"].append(
            {
                "type": "Deposit",
                "amount": amount,
                "time": current_time()
            }
        )
        save_data(data)
        print(f"Deposit successful. New balance: UGX {data['clients'][username]['balance']:.2f}")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


def withdraw(data, username):
    """Allow the logged-in user to withdraw money."""
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return

        balance = data["clients"][username]["balance"]

        if amount > balance:
            print("Insufficient funds.")
            return

        data["clients"][username]["balance"] -= amount
        data["clients"][username]["transactions"].append(
            {
                "type": "Withdrawal",
                "amount": amount,
                "time": current_time()
            }
        )
        save_data(data)
        print(f"Withdrawal successful. New balance: UGX {data['clients'][username]['balance']:.2f}")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


def view_balance(data, username):
    """Display the current balance of the logged-in user."""
    balance = data["clients"][username]["balance"]
    print(f"\nCurrent Balance: UGX {balance:.2f}")


def bank_summary(data, username):
    """Display a bank summary for the logged-in user."""
    client = data["clients"][username]
    print("\n========== BANK SUMMARY ==========")
    print(f"Client Name      : {client['full_name']}")
    print(f"Username         : {username}")
    print(f"Account Number   : {client['account_number']}")
    print(f"Current Balance  : UGX {client['balance']:.2f}")
    print(f"Total Transactions: {len(client['transactions'])}")


def transaction_history(data, username):
    """Display the transaction history of the logged-in user."""
    transactions = data["clients"][username]["transactions"]

    print("\n========== TRANSACTION HISTORY ==========")
    if not transactions:
        print("No transactions found.")
        return

    for index, transaction in enumerate(transactions, start=1):
        print(
            f"{index}. {transaction['type']} | "
            f"UGX {transaction['amount']:.2f} | "
            f"{transaction['time']}"
        )


def change_password(data, username):
    """Extra feature: allow the user to change their password."""
    old_password = input("Enter current password: ").strip()

    if data["clients"][username]["password"] != old_password:
        print("Incorrect current password.")
        return

    new_password = input("Enter new password: ").strip()
    confirm_password = input("Confirm new password: ").strip()

    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    if len(new_password) < 4:
        print("Password must be at least 4 characters long.")
        return

    data["clients"][username]["password"] = new_password
    save_data(data)
    print("Password changed successfully.")


def user_menu(data, username):
    """Display the operations menu for the logged-in user."""
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
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select a valid option.")


def main():
    """Main program entry point."""
    data = load_data()

    while True:
        print("\n========== SIMPLE BANKING SYSTEM ==========")
        print("1. Login")
        print("2. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            username = login(data)
            if username:
                user_menu(data, username)
        elif choice == "2":
            print("Thank you for using the banking system.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()