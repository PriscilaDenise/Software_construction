import logging
from storage import save_data, current_time
from exceptions import InvalidAmountError, InsufficientFundsError

logger = logging.getLogger(__name__)


def validate_amount(amount_text):
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise InvalidAmountError("Amount must be greater than zero.")
        return amount
    except ValueError as error:
        raise InvalidAmountError("Please enter a valid numeric amount.") from error


def deposit(data, username):
    amount = validate_amount(input("Enter amount to deposit: "))
    data["clients"][username]["balance"] += amount
    data["clients"][username]["transactions"].append({
        "type": "Deposit",
        "amount": amount,
        "time": current_time()
    })
    save_data(data)
    logger.info("Deposit successful for %s: %.2f", username, amount)
    print(f"Deposit successful. New balance: UGX {data['clients'][username]['balance']:.2f}")


def withdraw(data, username):
    amount = validate_amount(input("Enter amount to withdraw: "))
    balance = data["clients"][username]["balance"]

    if amount > balance:
        logger.warning("Withdrawal failed for %s due to insufficient funds.", username)
        raise InsufficientFundsError("Insufficient funds.")

    data["clients"][username]["balance"] -= amount
    data["clients"][username]["transactions"].append({
        "type": "Withdrawal",
        "amount": amount,
        "time": current_time()
    })
    save_data(data)
    logger.info("Withdrawal successful for %s: %.2f", username, amount)
    print(f"Withdrawal successful. New balance: UGX {data['clients'][username]['balance']:.2f}")


def view_balance(data, username):
    balance = data["clients"][username]["balance"]
    logger.info("Balance viewed by %s", username)
    print(f"\nCurrent Balance: UGX {balance:.2f}")


def change_password(data, username):
    old_password = input("Enter current password: ").strip()

    if data["clients"][username]["password"] != old_password:
        logger.warning("Password change failed for %s due to incorrect old password.", username)
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
    logger.info("Password changed successfully for %s", username)
    print("Password changed successfully.")