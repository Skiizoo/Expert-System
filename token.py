from enumerate import Type, Value
from display import display_infos
from error import SolveError


class Token:
    __instances = {}

    def __init__(self, char):
        self.char = char

    def __new__(cls, value):
        type_token = Type.from_value(value)
        if type_token is not Type.Letter:
            display_infos("Token.py", "__new__", "15", "Creation of specific Token operator " + value)
            instance = object.__new__(cls)
            instance.type = type_token
            if type_token is Type.Operator:
                instance.precedence = ['<=>', '=>', '^', '|', '+', '!'].index(value)
            return instance
        if value not in cls.__instances.keys():
            display_infos("Token.py", "__new__", "22", "Creation of global Token operator " + value)
            new_instance = object.__new__(cls)
            new_instance.type = type_token
            new_instance.rules = []
            new_instance.__value = Value.none
            cls.__instances[value] = new_instance
        else:
            display_infos("Token.py", "__new__", "28", "Global Token operator " + value + " already exists")
        return cls.__instances[value]

    def __gt__(self, other):
        return self.precedence > other.precedence

    def __lt__(self, other):
        return self.precedence < other.precedence

    def __str__(self):
        return self.char

    def __repr__(self):
        return self.char

    def __eq__(self, other):
        return self.char == other


    @property
    def value(self):
        if len(self.rules):
            display_infos("Token.py", "@property getter", "60", "We don't know yet the value of Token " + self.char)
            rule = self.rules.pop(0)
            str_rule = rule[1].split('=>')
            result = rule[0].left.get(str_rule[0])
            if result is not Value.false:
                rule[0].right.set(str_rule[1], result)
        display_infos("Token.py", "@property getter", "58", "Token " + self.char + " is " + str(self.__value))
        return self.__value

    @value.setter
    def value(self, new_value):
        if new_value != Value.ambiguous or self.__value is Value.none:
            if self.__value is Value.none or self.__value is Value.ambiguous or new_value is self.value:
                display_infos("Token.py", "@property setter", "68", "Token " + self.char + " is now " + str(new_value))
                self.__value = new_value
            else:
                raise SolveError("Token.py", "@property setter", "66", "Conflict value for Token " + self.char)

    @staticmethod
    def add(left, right, value, str_ccl):
        if value is Value.false:
            if right.get(str_ccl, ccl=True) is Value.true:
                left.set(str_ccl, value)
            elif left.get(str_ccl, ccl=True) is Value.true:
                right.set(str_ccl, value)
            else:
                left.set(str_ccl, Value.ambiguous)
                right.set(str_ccl, Value.ambiguous)
        else:
            right.set(str_ccl, value)
            left.set(str_ccl, value)

    @staticmethod
    def xor(left, right, value, str_ccl):
        if value is Value.ambiguous:
            left.set(str_ccl, value)
            right.set(str_ccl, value)
        else:
            right_ccl = right.get(str_ccl, ccl=True)
            left_ccl = left.get(str_ccl, ccl=True)
            if right_ccl is Value.true or right_ccl is Value.false:
                left.set(str_ccl, right_ccl if value is Value.false else ~right_ccl)
            elif left_ccl is Value.true or left_ccl is Value.false:
                right.set(str_ccl, left_ccl if value is Value.false else ~left_ccl)
            else:
                left.set(str_ccl, Value.ambiguous)
                right.set(str_ccl, Value.ambiguous)

    @staticmethod
    def oor(left, right, value, str_ccl):
        if value is Value.true and right.get(str_ccl, ccl=True) is Value.false:
            left.set(str_ccl, value)
        elif value is Value.true and left.get(str_ccl, ccl=True) is Value.false:
            right.set(str_ccl, value)
        elif value is Value.false:
            left.set(str_ccl, value)
            right.set(str_ccl, value)
        else:
            left.set(str_ccl, Value.ambiguous)
            right.set(str_ccl, Value.ambiguous)

    def get(self, str, ccl=False):
        display_infos("Token.py", "get", "73", "Solving Token " + self.char + " of expression " + str)
        if self == '!':
            return ~self.right.get(str, ccl)
        if self == '|':
            return self.left.get(str, ccl) | self.right.get(str, ccl)
        if self == '+':
            return self.left.get(str, ccl) & self.right.get(str, ccl)
        if self == '^':
            return self.left.get(str, ccl) ^ self.right.get(str, ccl)
        value = self.value
        if ccl is False:
            return value if value is not Value.none else Value.false
        return value

    def set(self, str, value=Value.true):
        display_infos("Token.py", "set", "86", "Solving Token " + self.char + " of conclusion " + str)
        if self == '+':
            self.add(self.left, self.right, value, str)
        elif self == '|':
            self.oor(self.left, self.right, value, str)
        elif self == '^':
            self.xor(self.left, self.right, value, str)
        elif self == '!':
            self.right.set(str, ~value)
        else:
            self.value = value
