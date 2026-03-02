import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any


@dataclass
class Transaction:
    item: str
    price: int
    category: str


class BaseCLI:

    def input_float(self, prompt: str) -> float:
        while True:
            raw = input(prompt).strip()
            try:
                return float(raw)
            except ValueError:
                print("Invalid number. Try again (e.g., 5000 or 12.50).")

    def input_non_negative_float(self, prompt: str) -> float:
        while True:
            value = self.input_float(prompt)
            if value < 0:
                print("Value cannot be less than 0.")
                continue
            return value

    def input_choice(self, prompt: str, choices: List[str]) -> str:
        choices_lower = [c.lower() for c in choices]
        while True:
            v = input(prompt).strip().lower()
            if v in choices_lower:
                return v
            print(f"Invalid choice. Choose one of: {', '.join(choices_lower)}")


class Budget:

    _MINIMUMS = {
        "daily": 5000.0,
        "weekly": 20000.0,
        "monthly": 50000.0,
    }

    def __init__(self, amount: float, period: str):
        self.__period = period.lower()
        self.__amount = amount

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def period(self) -> str:
        return self.__period

    @classmethod
    def minimum_for(cls, period: str) -> float:
        return cls._MINIMUMS[period.lower()]

    def remaining(self, total_spent: float) -> float:
        return self.__amount - total_spent

    def is_exceeded(self, total_spent: float) -> bool:
        return total_spent > self.__amount


class JsonStore:

    def __init__(self, filename: str = "expenditures.json"):
        self.path = Path(filename)

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {
                "budget": {"period": None, "amount": 0.0, "minimum": 0.0},
                "total_spent": 0.0,
                "categories": {"transport": [], "food": [], "data": [], "others": []},
            }

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            # If file is corrupted/unreadable, start fresh safely
            data = {
                "budget": {"period": None, "amount": 0.0, "minimum": 0.0},
                "total_spent": 0.0,
                "categories": {"transport": [], "food": [], "data": []},
            }

        # Ensure required keys exist
        data.setdefault("budget", {"period": None, "amount": 0.0, "minimum": 0.0})
        data.setdefault("total_spent", 0.0)
        data.setdefault("categories", {"transport": [], "food": [], "data": []})
        for cat in ["transport", "food", "data"]:
            data["categories"].setdefault(cat, [])

        return data

    def save(self, data: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class Ledger:

    def __init__(self, store: JsonStore):
        self._store = store
        self._data = self._store.load()

    @property
    def total_spent(self) -> float:
        return float(self._data.get("total_spent", 0.0))

    @property
    def categories(self) -> Dict[str, List[Dict[str, float]]]:
        return self._data["categories"]

    def set_budget_meta(self, period: str, amount: float, minimum: float) -> None:
        self._data["budget"] = {"period": period, "amount": float(amount), "minimum": float(minimum)}
        self._store.save(self._data)

    def add(self, tx: Transaction) -> None:
        self._data["categories"][tx.category].append({"item": tx.item, "price": float(tx.price)})
        self._data["total_spent"] = float(self.total_spent + tx.price)
        self._store.save(self._data)


class FinancialAssistant(BaseCLI):

    def __init__(self):
        self.__budget: Budget | None = None
        self.__store = JsonStore("expenditures.json")
        self.__ledger = Ledger(self.__store)
        self.__allowed_categories = ["transport", "food", "data"]

    def setup_budget(self) -> None:
        period = self.input_choice("Select budget period (daily/weekly/monthly): ", ["daily", "weekly", "monthly"])
        minimum = Budget.minimum_for(period)

        while True:
            amount = self.input_non_negative_float("Enter your budget: ")
            if amount < minimum:
                print(f"Minimum budget for {period} is {minimum:.0f}. Please enter {minimum:.0f} or more.")
                continue
            self.__budget = Budget(amount, period)
            self.__ledger.set_budget_meta(period, amount, minimum)
            print(f"Your {period} budget is {amount}")
            break

    def run_session(self) -> None:
        assert self.__budget is not None

        while True:
            item = input("\nWhat did you buy ? (type 'done' to finish): ").strip()
            if item.lower() == "done":
                break
            if item == "":
                print("Item cannot be empty.")
                continue

            category = self.input_choice("Category (transport/food/data/others): ", self.__allowed_categories)
            price = self.input_non_negative_float("Enter your price: ")

            self.__ledger.add(Transaction(item=item, price=price, category=category))

            if self.__budget.is_exceeded(self.__ledger.total_spent):
                print(f"WARNING: You exceeded your budget by {self.__ledger.total_spent - self.__budget.amount}")
                break
            else:
                print(f"Remaining budget: {self.__budget.remaining(self.__ledger.total_spent)}")

        self.print_summary()

    def print_summary(self) -> None:
        assert self.__budget is not None

        print("\n========================================== SUMMARY ====================================================")
        for cat, tx_list in self.__ledger.categories.items():
            print(f"\n[{cat.upper()}]")
            if not tx_list:
                print("  (no transactions)")
                continue
            for tx in tx_list:
                print(f"  You spent {tx['price']} on {tx['item']}")

        total_spent = self.__ledger.total_spent
        print(f"\nTotal spent: {total_spent}")

        if total_spent > self.__budget.amount:
            print("You exceeded your budget.")
        elif total_spent == self.__budget.amount:
            print("You reached your budget exactly.")
        else:
            print("You stayed within your budget.")

        print(f"Final balance: {self.__budget.remaining(total_spent)}")

    def system_loop(self) -> None:
        self.setup_budget()

        while True:
            self.run_session()
            resume = input("\nDo you want to resume? (yes/no): ").strip().lower()
            if resume != "yes":
                print("Goodbye!")
                break


if __name__ == "__main__":
    app = FinancialAssistant()
    app.system_loop()