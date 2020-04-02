from enum import Enum


class Type(Enum):
    Letter = 0
    Operator = 1
    LeftParen = 2
    RightParen = 3

    @classmethod
    def from_value(cls, value):
        if value == '(':
            return cls.LeftParen
        elif value == ')':
            return cls.RightParen
        elif value.isupper():
            return cls.Letter
        else:
            return cls.Operator

class Step(Enum):
    rules = 0
    facts = 1
    queries = 2

    def __next__(self):
        return None if self is Step.queries else Step(self.value + 1)
