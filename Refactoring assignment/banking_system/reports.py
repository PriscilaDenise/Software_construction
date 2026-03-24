import logging

logger = logging.getLogger(__name__)


def bank_summary(data, username):
    client = data["clients"][username]
    logger.info("Bank summary viewed by %s", username)
    print("\n========== BANK SUMMARY ==========")
    print(f"Client Name       : {client['full_name']}")
    print(f"Username          : {username}")
    print(f"Account Number    : {client['account_number']}")
    print(f"Current Balance   : UGX {client['balance']:.2f}")
    print(f"Total Transactions: {len(client['transactions'])}")


def transaction_history(data, username):
    transactions = data["clients"][username]["transactions"]
    logger.info("Transaction history viewed by %s", username)

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