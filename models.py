from datetime import datetime

class Transaction:
    def __init__(self, amount: float, category: str, date: str,
                 comment: str = "", transaction_id: int | None = None):
        self.amount = amount
        self.category = category
        self.date = date
        self.comment = comment.strip()
        self.id = transaction_id

    @property
    def amount(self):
        return self.__amount
    @property
    def category(self):
        return self.__category
    @property
    def date(self):
        return self.__date

    @amount.setter
    def amount(self, amount: float):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("amount ნულზე მეტი უნდა იყოს>")
        else:
            amount = round(float(amount), 2)
        self.__amount = amount

    @category.setter
    def category(self, category: str):
        if not category or not category.strip():
            raise ValueError("კატეგორია ცარიელია????")
        self.__category = category.strip()

    @date.setter
    def date(self, date: str):
        try:
            datetime.strptime(date.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValueError("თარიღი უნდა იყოს ფორმატში YYYY-MM-DD!")
        self.__date = date.strip()

    def get_type(self) -> str:
        return "ტრანზაქცია"

    def to_dict(self) -> dict:
        return {"id": self.id, "type": self.get_type(),
                "amount": self.amount, "category": self.category,
                "date": self.date, "comment": self.comment}
    def __str__(self) -> str:
        return (f"{self.id} {self.date} {self.get_type()} "
                f"{self.category} {self.amount} {self.comment}")

    def get_signed_amount(self) -> float:
        return self.amount

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        target_cls = Income if data.get("type") == "შემოსავალი" else Expense
        return target_cls(
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            comment=data.get("comment", ""),
            transaction_id=data.get("id")
        )

class Income(Transaction):
    def get_type(self) -> str:
        return "შემოსავალი"
    def get_signed_amount(self) -> float:
        return +self.amount

class Expense(Transaction):
    def get_type(self) -> str:
        return "ხარჯი"
    def get_signed_amount(self) -> float:
        return -self.amount