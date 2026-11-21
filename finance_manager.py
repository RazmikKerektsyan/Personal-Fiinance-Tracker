import json
import os
from models import Transaction, Income, Expense
from decorators import auto_save, validate_month

class FinanceManager:
    def __init__(self, filename: str = "finance.json"):
        self.filename = filename
        self.transactions: list[Transaction] = []
        self.budgets: dict[str, float] = {}
        self.load_from_file()

    def get_next_id(self) -> int:
        if not self.transactions:
            return 1
        else:
            return max((t.id or 0) for t in self.transactions) +1

    def save_to_file(self):
        tx_list = []
        for t in self.transactions:
            tx_list.append(t.to_dict())
        data = {
            "transactions": tx_list,
            "budgets": self.budgets
        }
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_from_file(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.transactions = []
                for item in data.get("transactions", []):
                    self.transactions.append(Transaction.from_dict(item))
                self.budgets = data.get("budgets", {})
        except (json.JSONDecodeError, KeyError, ValueError):
            self.transactions = []
            self.budgets = {}

    @auto_save
    def add_income(self, amount: float, category: str, date: str, description: str = ""):
        income = Income(amount, category, date, description, self.get_next_id())
        self.transactions.append(income)
        return income

    @auto_save
    def add_expense(self, amount: float, category: str, date: str, description: str = ""):
        expense = Expense(amount, category, date, description, self.get_next_id())
        self.transactions.append(expense)
        return expense

    @auto_save
    def delete_transaction(self, transaction_id: int) -> bool:
        for t in self.transactions:
            if t.id == transaction_id:
                self.transactions.remove(t)
                return True
        return False

    @auto_save
    def set_budget(self, category: str, limit: float):
        if limit <= 0:
            raise ValueError("ბიუჯეტის ლიმიტი უნდა იყოს დადებითი რიცხვი!")
        self.budgets[category.strip()] = float(limit)

    @validate_month
    def get_transaction_month(self, month: str) -> list[Transaction]:
        result = []
        for t in self.transactions:
            if t.date.startswith(month):
                result.append(t)
        return result

    @validate_month

    def get_monthly_budget(self, month: str) -> dict:
        tx_list = self.get_transaction_month(month)
        total_income = 0.0
        total_expense = 0.0
        for t in tx_list:
            if isinstance(t, Income):
                total_income += t.amount
            elif isinstance(t, Expense):
                total_expense += t.amount
        return {"total_income": total_income, "total_expense": total_expense, "balance": total_income - total_expense}

    @validate_month
    def check_budget(self, month: str) -> list[dict]:
        tx_list = self.get_transaction_month(month)
        report = []
        for category, limit in self.budgets.items():
            spent = 0.0
            for t in tx_list:
                if isinstance(t, Expense) and t.category == category:
                    spent += t.amount
            report.append({
                "category": category,
                "limit": limit,
                "spent": spent,
                "exceeded": spent > limit,
            })
        return report




