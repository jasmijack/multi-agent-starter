from src.core import Tool

class Calculator(Tool):
    def __init__(self):
        super().__init__("calculator", "Basic arithmetic like 2+2 or 7*6")
    def __call__(self, expr: str) -> str:
        allowed = set("0123456789+-*/(). ")
        if not set(expr) <= allowed:
            raise ValueError("Disallowed characters in expression")
        return str(eval(expr))
