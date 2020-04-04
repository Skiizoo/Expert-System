from enumerate import Type, Value
from display import display_infos, display_tree, display_treeV2
from error import SolveError
import re


def my_max(tab):
    maximum = 0
    if not tab:
        return maximum
    for t in tab:
        for j in t:
            if maximum < j[1]:
                maximum = j[1]
    return maximum


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
            cls.__instances[value] = object.__new__(cls)
            cls.__instances[value].type = type_token
            cls.__instances[value].rules = [[None, None]]
            cls.__instances[value].__value = Value.none
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
        if len(self.rules) == 1:
            display_infos("Token.py", "@property getter", "58", "Token " + self.char + " is " + str(self.__value))
            return self.__value
        display_infos("Token.py", "@property getter", "60", "We don't know yet the value of Token " + self.char)
        return self.calc()

    @value.setter
    def value(self, new_value):
        if new_value != Value.ambiguous or self.__value is Value.none:
            if self.__value is not Value.none and self.__value is not Value.ambiguous and self.__value is not new_value:
                print("error")
                raise SolveError("Token.py", "@property setter", "66", "Conflict value for Token " + self.char)
            self.__value = new_value
            display_infos("Token.py", "@property setter", "68", "Token " + self.char + " is now " + str(new_value))
            if len(self.rules) > 1:
                self.__value = self.calc()

    @staticmethod
    def add(left, right, value, str_ccl):
        if value is Value.false:
            if right.calc_conclusion(str_ccl) is Value.true:
                left.solve(str_ccl, value)
            elif left.calc_conclusion(str_ccl) is Value.true:
                right.solve(str_ccl, value)
            else:
                left.solve(str_ccl, Value.ambiguous)
                right.solve(str_ccl, Value.ambiguous)
        else:
            right.solve(str_ccl, value)
            left.solve(str_ccl, value)

    @staticmethod
    def xor(left, right, value, str_ccl):
        if value is Value.ambiguous:
            left.solve(str_ccl, value)
            right.solve(str_ccl, value)
        else:
            right_ccl = right.calc_conclusion(str_ccl)
            left_ccl = left.calc_conclusion(str_ccl)
            if right_ccl is Value.none and left_ccl is Value.none:
                left.solve(str_ccl, Value.ambiguous)
                right.solve(str_ccl, Value.ambiguous)
            elif right_ccl is not Value.none:
                left.solve(str_ccl, right_ccl if value is Value.false else ~right_ccl)
            elif left_ccl is not Value.none:
                right.solve(str_ccl, left_ccl if value is Value.false else ~left_ccl)

    @staticmethod
    def oor(left, right, value, str_ccl):
        if value is Value.true and right.calc_conclusion(str_ccl) is Value.false:
            left.solve(str_ccl, value)
        elif value is Value.true and left.calc_conclusion(str_ccl) is Value.false:
            right.solve(str_ccl, value)
        elif value is Value.false:
            left.solve(str_ccl, value)
            right.solve(str_ccl, value)
        else:
            left.solve(str_ccl, Value.ambiguous)
            right.solve(str_ccl, Value.ambiguous)

    def calc_expression(self, str_expr):
        display_infos("Token.py", "calc_expression", "73", "Solving Token " + self.char + " of expression " + str_expr)
        if self == '!':
            return ~self.right.calc_expression(str_expr)
        elif self == '|':
            return self.left.calc_expression(str_expr) | self.right.calc_expression(str_expr)
        elif self == '+':
            return self.left.calc_expression(str_expr) & self.right.calc_expression(str_expr)
        elif self == '^':
            return self.left.calc_expression(str_expr) ^ self.right.calc_expression(str_expr)
        return Value.default(self.value)

    def calc_conclusion(self, str_ccl):
        display_infos("Token.py", "calc_conclusion", "73", "Solving Token " + self.char + " of expression " + str_ccl)
        if self == '!':
            return self.right.calc_conclusion(str_ccl).neg_ccl()
        elif self == '|':
            return self.left.calc_conclusion(str_ccl).or_ccl(self.right.calc_conclusion(str_ccl))
        elif self == '+':
            return self.left.calc_conclusion(str_ccl).and_ccl(self.right.calc_conclusion(str_ccl))
        elif self == '^':
            return self.left.calc_conclusion(str_ccl).xor_ccl(self.right.calc_conclusion(str_ccl))
        else:
            return Value.default_ccl(self.value)

    def solve(self, str_ccl, value=Value.true):
        display_infos("Token.py", "solve", "86", "Solving Token " + self.char + " of conclusion " + str_ccl)
        if self == '+':
            self.add(self.left, self.right, value, str_ccl)
        elif self == '|':
            self.oor(self.left, self.right, value, str_ccl)
        elif self == '^':
            self.xor(self.left, self.right, value, str_ccl)
        elif self == '!':
            self.right.solve(str_ccl, ~value)
        else:
            self.value = value

    def calc(self):
        display_infos("Token.py", "calc", "97", "Looking for Token " + self.char + "'s value")
        token = self.rules.pop(0)
        if token[0] is not None:
            display_infos("Token.py", "calc", "100", "Looking into Token " + self.char + "'s rule: " + token[1])
            str_rule = token[1].split('=>')
            result = token[0].left.calc_expression(str_rule[0])
            if result is not Value.false:
                token[0].right.solve(str_rule[1], result)
        return self.value

    def display(self, rules, depth, token=None, tab=[], init=False):
        if token is not None:
            if depth > len(tab):
                tab.append([])
            if depth == 0 and len(rules) > 1:
                self.display(rules, 1, rules.pop(0)[0], tab, True)
            elif token.type is Type.Operator:
                self.display(rules, depth + 1, token.right, tab, True)
                display_tree(token.char, depth)
                tab[depth - 1].append([token.char, my_max(tab) + 1])
                if self.char != "!":
                    self.display(rules, depth + 1, token.left, tab, True)
                if depth == 1 and len(rules) > 1:
                    self.display(rules, 1, rules.pop(0)[0], tab, True)
            elif token.type is Type.Letter:
                display_tree(token.char, depth)
                tab[depth - 1].append([token.char, my_max(tab) + 1])
        # todo print
        # if init is False:
        # display_treeV2(tab)
