from enumerate import Type
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
            cls.__instances[value].__value = None
        else:
            display_infos("Token.py", "__new__", "28", "Global Token operator " + value + " already exists")
        return cls.__instances[value]

    def __gt__(self, other):
        return self.precedence > other.precedence

    def __lt__(self, other):
        return self.precedence < other.precedence

    def __le__(self, other):
        return self.precedence <= other.precedence

    def __ge__(self, other):
        return self.precedence >= other.precedence

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
        print(self, new_value, self.__value)
        if new_value == "Ambiguous" and self.__value is not None:
            pass
        else:
            if self.__value is not None and self.__value != "Ambiguous" and self.__value != new_value:
                print("error")
                raise SolveError("Token.py", "@property setter", "66", "Conflict value for Token " + self.char)
            self.__value = new_value
            display_infos("Token.py", "@property setter", "68", "Token " + self.char + " is now " + str(new_value))
            if len(self.rules) > 1:
                self.__value = self.calc()

    def calc_expression(self, str_expr):
        display_infos("Token.py", "calc_expression", "73", "Solving Token " + self.char + " of expression " + str_expr)
        if self == '!':
            right = self.right.calc_expression(str_expr)
            if right == "Ambiguous":
                return "Ambiguous"
            return not right
        elif self == '|':
            left = self.left.calc_expression(str_expr)
            right = self.right.calc_expression(str_expr)
            if left is True or right is True:
                return True
            if left == "Ambiguous" or right == "Ambiguous":
                return "Ambiguous"
            return False
        elif self == '+':
            left = self.left.calc_expression(str_expr)
            right = self.right.calc_expression(str_expr)
            if left == "Ambiguous" or right == "Ambiguous":
                return "Ambiguous"
            return left and right
        elif self == '^':
            left = self.left.calc_expression(str_expr)
            right = self.right.calc_expression(str_expr)
            if left == "Ambiguous" or right == "Ambiguous":
                return "Ambiguous"
            return left is not right
        else:
            value = self.value
            return value if value is not None else False

    def calc_conclusion(self, str_ccl):
        display_infos("Token.py", "calc_conclusion", "73", "Solving Token " + self.char + " of expression " + str_ccl)
        if self == '!':
            right = self.right.calc_conclusion(str_ccl)
            if right is None:
                return right
            return not right
        elif self == '|':
            left = self.left.calc_conclusion(str_ccl)
            right = self.right.calc_conclusion(str_ccl)
            if left is True or right is True:
                return True
            if left is None or right is None:
                return None
            return False
        elif self == '+':
            left = self.left.calc_conclusion(str_ccl)
            right = self.right.calc_conclusion(str_ccl)
            if left is None or right is None:
                return None
            return left and right
        elif self == '^':
            left = self.left.calc_conclusion(str_ccl)
            right = self.right.calc_conclusion(str_ccl)
            if left is None or right is None:
                return None
            return left is not right
        else:
            value = self.value
            return value if value != "Ambiguous" else None

    def solve(self, str_ccl, value=True):
        display_infos("Token.py", "solve", "86", "Solving Token " + self.char + " of conclusion " + str_ccl)
        # todo: xor
        if self == '+':
            if value is False:
                if self.right.calc_conclusion(str_ccl) is True:
                    self.left.solve(str_ccl, value)
                elif self.left.calc_conclusion(str_ccl) is True:
                    self.right.solve(str_ccl, value)
                else:
                    self.left.solve(str_ccl, "Ambiguous")
                    self.right.solve(str_ccl, "Ambiguous")
            else:
                self.right.solve(str_ccl, value)
                self.left.solve(str_ccl, value)
        elif self == '|':
            if value is False:
                self.right.solve(str_ccl, value)
                self.left.solve(str_ccl, value)
            elif value is True and self.right.calc_conclusion(str_ccl) is False:
                self.left.solve(str_ccl, value)
            elif value is True and self.left.calc_conclusion(str_ccl) is False:
                self.right.solve(str_ccl, value)
            else:
                self.left.solve(str_ccl, "Ambiguous")
                self.right.solve(str_ccl, "Ambiguous")
        elif self == '^':
            if value is False:
                pass
            #todo: not xor
            elif value == "Ambiguous":
                self.left.solve(str_ccl, "Ambiguous")
                self.right.solve(str_ccl, "Ambiguous")
            else:
                right = self.right.calc_conclusion(str_ccl)
                left = self.left.calc_conclusion(str_ccl)
                if right is True or right is False:
                    self.left.solve(str_ccl, not right)
                elif left is True or left is False:
                    self.right.solve(str_ccl, not left)
                else:
                    self.left.solve(str_ccl, "Ambiguous")
                    self.right.solve(str_ccl, "Ambiguous")
        elif self == '!':
            if value == "Ambiguous":
                self.right.solve(str_ccl, "Ambiguous")
            else:
                self.right.solve(str_ccl, not value)
        else:
            self.value = value

    def calc(self):
        print(self)
        display_infos("Token.py", "calc", "97", "Looking for Token " + self.char + "'s value")
        token = self.rules.pop(0)
        if token[0] is not None:
            display_infos("Token.py", "calc", "100", "Looking into Token " + self.char + "'s rule: " + token[1])
            str_rule = token[1].split('=>')
        result = None
        if token[0] is not None:
            result = token[0].left.calc_expression(str_rule[0])
        if result is True or result == 'Ambiguous':
            token[0].right.solve(str_rule[1], result)
        elif self.value is True or self.value == "Ambiguous":
            token[0].right.solve(str_rule[1], self.value)
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
        #if init is False:
            #display_treeV2(tab)




