from enum import Enum


class Value(Enum):
    false = 0,
    true = 1,
    ambiguous = 2,
    none = 3

    def __str__(self):
        switch = {
            Value.false: "False",
            Value.true: "True",
            Value.ambiguous: "Ambiguous"
        }
        return switch.get(self, "False")

    def __invert__(self):
        if self is Value.ambiguous:
            return Value.ambiguous
        if self is Value.none:
            return Value.none
        if self is Value.true:
            return Value.false
        return Value.true

    def __or__(self, other):
        if self is Value.true or other is Value.true:
            return Value.true
        if self is Value.none or right is Value.none:
            return Value.none
        if self is Value.ambiguous or other is Value.ambiguous:
            return Value.ambiguous
        return Value.false

    def __and__(self, other):
        if self is Value.ambiguous or other is Value.ambiguous:
            return Value.ambiguous
        if self is Value.none or other is Value.none:
            return Value.none
        if self is Value.true and other is Value.true:
            return Value.true
        return Value.false

    def __xor__(self, other):
        if self is Value.ambiguous or other is Value.ambiguous:
            return Value.ambiguous
        if self is Value.none or other is Value.none:
            return Value.none
        if self is not other:
            return Value.true
        return Value.false

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
