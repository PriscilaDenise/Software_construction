def financial_assistant():

    budget = float(input("Enter your budget: ")) # User input for budget

    # Error handling to ensure budget is not less than 0
    while budget < 0:
        print("Budget cannot be less than 0.")
        budget = float(input("Enter your budget: "))

    print(f"Your budget is {budget}") # Display budget

    expenditures = {} # Dictionary to store expenditures
    total_spent = 0 # Variable to track total spent


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

    # Display final summary
    print("\n========================================== FINAL SUMMARY ====================================================")


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




financial_assistant()