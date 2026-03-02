# budget function
def budget():

    budget = float(input("Enter your budget: "))  # User input for budget

    # Error handling to ensure budget is not less than 0
    while budget < 0:
        print("Budget cannot be less than 0.")
        budget = float(input("Enter your budget: "))

    print(f"Your budget is {budget}")  # Display budget

    return budget

# financial assistant function
def financial_assistant(budget, expenditures, total_spent):

    # Loop to get expenditures
    while True:

        item = input("\nWhat did you buy ? (type 'done' to finish): ")

        if item.lower() == "done":
            break

        price = float(input("Enter your price: "))

        expenditures[item] = price
        total_spent += price

        if total_spent > budget:
            print(f"WARNING: You exceeded your budget by {total_spent - budget}")
        else:
            print(f"Remaining budget: {budget - total_spent}")

    # Display summary 
    print("\n========================================== SUMMARY ====================================================")

    for item, price in expenditures.items():
        print(f"You spent {price} on {item}")

    print(f"\nTotal spent: {total_spent}")

    if total_spent > budget:
        print("You exceeded your budget.")
    elif total_spent == budget:
        print("You reached your budget exactly.")
    else:
        print("You stayed within your budget.")

    print(f"Final balance: {budget - total_spent}")

    return expenditures, total_spent

# main function
def system():

    user_budget = budget()

    expenditures = {}   # stays in memory across resumes
    total_spent = 0.0   # stays in memory across resumes

    while True:
        expenditures, total_spent = financial_assistant(user_budget, expenditures, total_spent)

        resume = input("\nDo you want to resume? (yes/no): ").lower()

        if resume != "yes":
            print("Goodbye!")
            break

# Call the main function
system()