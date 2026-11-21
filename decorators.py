from functools import wraps
from datetime import datetime


def auto_save(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.save_to_file()
        return result
    return wrapper

def validate_month(func):
    @wraps(func)
    def wrapper(self, month: str,*args, **kwargs):
        try:
            datetime.strptime(month.strip(), "%Y-%m")
        except ValueError:
            raise ValueError("თვე უნდა იყოს ფორმატში YYYY-MM (მაგ: 2026-11)!")
        return func(self, month, *args, **kwargs)

    return wrapper