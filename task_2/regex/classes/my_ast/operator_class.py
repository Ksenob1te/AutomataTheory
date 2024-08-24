from enum import Enum
from typing import Set


class Operator:
    class Type(Enum):
        CONCAT = 1
        ALTER = 2
        PREDICTIVE = 3
        REPEAT = 4
        SET_RANGE = 5

    @classmethod
    def check_operator(cls, operator: str) -> bool:
        return operator in ['+', '*', '|', '/', ''] or (operator[0] == '{' and operator[-1] == '}') or (operator[0] == '[' and operator[-1] == ']')

    type: Type = None
    set_range: Set = None
    min_repetitions: int | None = None
    max_repetitions: int | None = None

    def __new__(cls, *args, operator: str = None, **kwargs):
        if operator is None and len(args) == 1:
            operator = args[0]
        if operator is not None and cls.check_operator(operator):
            return super().__new__(cls)
        return None

    def __init__(self, operator: str):
        if operator == '+':
            self.type = Operator.Type.REPEAT
            self.min_repetitions = 1
            self.max_repetitions = None
        elif operator == '*':
            self.type = Operator.Type.REPEAT
            self.min_repetitions = 0
            self.max_repetitions = None
        elif len(operator) > 0 and operator[0] == '{' and operator[-1] == '}':
            operator = operator[1:-1]
            self.type = Operator.Type.REPEAT
            if "," in operator:
                left, right = operator.split(',')
                left = left.replace(" ", "")
                right = right.replace(" ", "")
                self.min_repetitions = int(left) if left.isdigit() else 0
                self.max_repetitions = int(right) if right.isdigit() else 0
            else:
                self.min_repetitions = int(operator) if operator.isdigit() else 0
                self.max_repetitions = int(operator) if operator.isdigit() else 0
        elif operator == "|":
            self.type = Operator.Type.ALTER
        elif operator == "":
            self.type = Operator.Type.CONCAT
        elif operator == "/":
            self.type = Operator.Type.PREDICTIVE
        elif len(operator) > 0 and operator[0] == '[' and operator[-1] == ']':
            operator = operator[1:-1]
            self.set_range = set()
            self.type = Operator.Type.SET_RANGE
            i: int = 0
            while i < len(operator):
                if i != 0 and operator[i] == '-':
                    if i != len(operator) - 1 and operator[i - 1] < operator[i + 1]:
                        for char in range(ord(operator[i - 1]), ord(operator[i + 1]) + 1):
                            self.set_range.add(chr(char))
                        i += 1
                    else:
                        self.set_range.add(operator[i])
                else:
                    self.set_range.add(operator[i])
                i += 1



    def __str__(self):
        return self.type.name
