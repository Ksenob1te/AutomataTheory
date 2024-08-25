from enum import Enum

# TODO: change to throw exceptions
class Status(Enum):
    OK = 0
    WRONG_OPERATOR = 1
    INCORRECT_AST = 2
    WRONG_STATE_SET = 3